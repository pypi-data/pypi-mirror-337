#!/usr/bin/env python3
import http.server
import socket
import json
import logging
import os
import subprocess
import time
import threading
from multiprocessing import Queue
#from queue import Queue
import  psutil
import sys
import signal
import urllib.parse
DBGMSG = True
WORK_DIR = "/home/psydow/bworker/workDir"
# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')
            
def IsChildrenRunning(children, timeout=10):
    try:
        for processId in children:
            children[processId].wait(timeout=timeout)
            if DBGMSG:
                print("[dbg]: all children has been closed", flush=True)
    except:
        if DBGMSG:
            print("[dbg]: Child {} has not ben closed by its parent".format(children[processId].pid), flush=True)
        return True
    return False

def kill_child_processes(children, sig=signal.SIGTERM):
    for processId in children:
         try:
             if DBGMSG:
                 print("[dbg]: Killing child process: {}".format(children[processId].pid), flush=True)
             sys.stdout.flush()
             children[processId].send_signal(sig)
         except:
             pass

def transcriptFunction(line):
    print("transcriptFunction kuku:>", line)

def backgroundMonitor(q,qout,proc,t1,t2, cmd,timeout, transcriptFunction):
    parent = psutil.Process(proc.pid)
    if DBGMSG:
        print("[dbg]: backgroundMonitor started for {} ".format(proc.pid), flush=True)
    sys.stdout.flush()
    childMap={}
    errorCode = 0
    secCounter = timeout/1000

    while(True):
        data = None
        try:
            data = q.get(block=False)
        except:
            data = None
            
        try:
            proc.wait(timeout=1)
            returnCode = proc.returncode
            t1.join()
            t2.join()
            qout.put({"returncode":returnCode})
            if DBGMSG:
               print("[dbg]: send return code",returnCode, flush=True)
            break
        
        except subprocess.TimeoutExpired:
            if secCounter > 0:
                secCounter = secCounter -1
            if secCounter == 0:
                print("[1] send stop signal!!!")
                q.put("stop")
                transcriptFunction("[remote]> remote job ({}) has timeouted.".format(cmd))
            pass

        children = parent.children(recursive=True)
        for child in children:
            if child.pid not in childMap:
                if DBGMSG:
                    print("[dbg]: Detect new child: {}".format(child.pid), flush=True)
                sys.stdout.flush()
                childMap[child.pid] = child

        disappiredChildren=[]
        for childPid in childMap:
            if not childMap[childPid].is_running():
                if DBGMSG:
                    print("[dbg]: Child process '{}' has gone.".format(childPid), flush=True)
                disappiredChildren.append(childPid)
                sys.stdout.flush()
        for childPid in disappiredChildren:
            childMap.pop(childPid, None)


        if data:        
            try:
                proc.wait(timeout=1.3)
                if DBGMSG:
                    print("[dbg]: The background process '{}' ({}) has been closed unexpectedly".format(cmd, proc.pid), flush=True)
                q.put("The background process '{}' ({}) has been closed unexpectedly".format(cmd, proc.pid))

            except subprocess.TimeoutExpired:
                if DBGMSG:
                    print("[dbg]: Proces {} is running".format(proc.pid), flush=True)
            
            if DBGMSG:
                print("[dbg]: Going to send kill signal to :{}".format(proc.pid), flush=True)  
            sys.stdout.flush() 
            proc.send_signal(signal.SIGINT)
            if DBGMSG:
                print("[dbg]: Waiting for finish:{}".format(proc.pid), flush=True)

            try:
                proc.wait(timeout=10)
                if DBGMSG:
                    print("[dbg]: seems that main process '{}' has been closed sucessfully. Let's join it".format(proc.pid), flush=True)
                sys.stdout.flush()
            except subprocess.TimeoutExpired:
                q.put("The main proces '{}' has not been closed sucessfully".format(proc.pid))
                if DBGMSG:
                    print("[dbg]: The main proces '{}' has not been closed sucessfully".format(proc.pid), flush=True)
                    print("[dbg]: Let's kill it.", flush=True)
                sys.stdout.flush()
                proc.send_signal(signal.SIGKILL)


            if IsChildrenRunning(childMap):
                if DBGMSG:
                    print("[dbg]: Closeing children of {} process".format(proc.pid), flush=True)
                kill_child_processes(childMap)
            if DBGMSG:
                print("[dbg]: Joining... {} ".format(proc.pid), flush=True)
            sys.stdout.flush()
        #timeoutFlag=True
            t1.join()
            t2.join()
            if DBGMSG:
                print("[dbg]: Process {} has been fully joined".format(proc.pid), flush=True)
            q.put("")
            returnCode = proc.returncode
            if returnCode == None:
                returnCode = 9
            qout.put({"returncode":returnCode})
            if DBGMSG:
                print("[dbg]: [2] send return code",returnCode, flush=True)
            break

def getArgs(s):
    args = []
    cur  = ''
    inQuotes = 0
    for char in s.strip():
        if char == ' ' and not inQuotes:
            args.append(cur)
            cur = ''
        elif char == '"' and not inQuotes:
            inQuotes = 1
            #cur += char
        elif char == '"' and inQuotes:
            inQuotes = 0
            #cur += char
        else:
            cur += char
    args.append(cur)
    return args


def streamReader(pipe,stdoutQueue):
    while True:
        time.sleep(0.1)
        #print("wait for line")
        #sys.stdout.flush()
        line = pipe.readline()
        #print("got line: '{}'".format(line))
        #sys.stdout.flush()
        if line:
            stdoutQueue.put(line.rstrip())
            print("kuku> ", line.rstrip())          
        if (not line):
            break



def findJobById(IP):
    for jobId in JobContainer:
        if "IP" in JobContainer[jobId]:
            if JobContainer[jobId]["IP"] == IP:
                return jobId
    return None


class ThreadSafeDict:
    def __init__(self):
        self._dict = {}
        self._lock = threading.RLock()

    def __iter__(self):
        # Return an iterator over a safe copy of the keys
        with self._lock:
            keys_snapshot = list(self._dict.keys())
        return iter(keys_snapshot)
    
    def to_dict(self):
        with self._lock:
            return self._dict.copy()
        
    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value

    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]

    def __delitem__(self, key):
        with self._lock:
            del self._dict[key]

    def __contains__(self, key):
        with self._lock:
            return key in self._dict

    def items(self):
        with self._lock:
            return list(self._dict.items())

    def keys(self):
        with self._lock:
            return list(self._dict.keys())

    def values(self):
        with self._lock:
            return list(self._dict.values())

    def __len__(self):
        with self._lock:
            return len(self._dict)

    def clear(self):
        with self._lock:
            self._dict.clear()

    def pop(self, key, default=None):
        with self._lock:
            return self._dict.pop(key, default)
        
class CMDExecutor():
    def __init__(self):
        self.backgroundActionsToKill=ThreadSafeDict()


    def getPidBuId(self, id):
        data = None
        if id not in self.backgroundActionsToKill.to_dict():
            return None
        data = self.backgroundActionsToKill[id]['pid']
        return data
    
    def getProcessreturnCode(self, id):
        data = None
        if id not in self.backgroundActionsToKill.to_dict():
            if DBGMSG:
                print("[dbg]: job has not been found in backgroundActionsToKill",id, flush=True)
            return None
        
        try:
            data = self.backgroundActionsToKill[id]['backgroundMonitorOut'].get(block=False)
            if DBGMSG:
                print("[dbg]: get data from backgroundMonitorOut",data, flush=True)
        except:
            data = None
        
        if data and 'returncode' in data:
            if DBGMSG:
                print("[dbg]: return code has been recived. proces record will be deleted",data, flush=True)
            self.backgroundActionsToKill.pop(id)
            return data["returncode"];
        return None;

#self.backgroundActionsToKill[jobId] = {"q":q,"backgroundMonitorOut":qout,"backgroundMonitor":t3,"proc":proc}
    def killBackgroundedById(self, id):
        if id not in self.backgroundActionsToKill.to_dict():
            return 
        
        if DBGMSG:
            print("[dbg]: Send kill message to q for job {}".format(id), flush=True)
        self.backgroundActionsToKill[id]["q"].put("stop")


        return 


    def shellCmd(self,command,jobId, transcriptFunction,env=None,timeout=1200):
        if jobId in self.backgroundActionsToKill.to_dict():
            print("Error: ynable to execute shellCmd. Job id {} already defined.".format(jobId))
            return -1
        
        cmdSplit = getArgs(command) #command.split()
        cmdName = os.path.basename(cmdSplit[0])

        finalEnv = {}
        for item in os.environ:
            finalEnv[item] =os.environ[item]

        if env:
            for item in env:
                finalEnv[item] =env[item]

        timeoutFlag=False
        oldPath = os.getcwd()
        success = False
        
        try:
            proc = subprocess.Popen(cmdSplit,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,env=finalEnv, bufsize=1, universal_newlines=True)
            success = True
        except FileNotFoundError:
            transcriptFunction("[bfan]> Command '{}' not found!!!.".format(cmdSplit[0]))
            return -1


        os.chdir(oldPath)
        stdoutQueue = Queue()
        t1 = threading.Thread(target=streamReader, args=[proc.stdout, stdoutQueue])
        t2 = threading.Thread(target=streamReader, args=[proc.stderr, stdoutQueue])
       
        
        t1.start()
        t2.start()
        


        q = Queue()
        qout = Queue()
        
        t3 = threading.Thread(target = backgroundMonitor, args =(q,qout,proc,t1,t2, cmdName, timeout, transcriptFunction))
        t3.start()
        self.backgroundActionsToKill[jobId] = {"pid":proc.pid, "stdoutQueue":stdoutQueue,"q":q,"backgroundMonitorOut":qout,"backgroundMonitor":t3,"proc":proc}
   
        return proc.pid,stdoutQueue



cmdExecutor = CMDExecutor()    
JobContainer=ThreadSafeDict()
JobCounter=1


class CustomHandler(http.server.BaseHTTPRequestHandler):
    # def __init__(self,a,b,c):
    #     super().__init__(a,b,c)  
    def refresh(self, jobId):
        if jobId in JobContainer:
            if not JobContainer[jobId]['WDTimeout']:
                JobContainer[jobId]['refreshTime'] = time.time()

    def clenup(self):
        jobsToRemove=[]
        for jobId in JobContainer:
            timeElapsed = time.time() - JobContainer[jobId]["refreshTime"]
            if timeElapsed > 10:
                if JobContainer[jobId]['state'] not in  ['RUNNING','KILLING']:
                    jobsToRemove.append(jobId)
                elif JobContainer[jobId]['state'] != 'KILLING':
                    if DBGMSG:
                        print("[dbg]: Time out on job {}. let's kill it".format(jobId), flush=True)
                    JobContainer[jobId]['state'] = 'KILLING'     
                    cmdExecutor.killBackgroundedById(jobId)
                    JobContainer[jobId]['WDTimeout'] = True

        for job in jobsToRemove:
            JobContainer.pop(job)

    def updateProcessReturnCode(self):
        for jobId in JobContainer:
            returnCode = cmdExecutor.getProcessreturnCode(jobId);

            if  returnCode != None:
                if DBGMSG:
                    print("[dbg]: unable to udate return code. No jobID", flush=True)
                JobContainer[jobId]["pid"]=None
                JobContainer[jobId]["returnCode"]=returnCode
                JobContainer[jobId]["state"]="DONE"

    def do_GET(self):
        self.updateProcessReturnCode()
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query_params = urllib.parse.parse_qs(parsed_url.query)

        global JobCounter
        global JobContainer
        global cmdExecutor
        client_ip = self.client_address[0]
        print(path)
        if path == '/sink':
            jobId = query_params.get('jobId', [None])[0]
            self.refresh(jobId)
            self.clenup()
            stdoutQueue = JobContainer[jobId]['stdoutQueue']
            response=[]
            if stdoutQueue != None:
                try:
                    response = stdoutQueue.get(block=False)
                except:
                    response = None

            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        if path == '/startJob':
            #query_params = parse_qs(parsed_url.query)
            jobId = query_params.get('jobId', [None])[0]
            self.refresh(jobId)
            self.clenup()
            testName = query_params.get('testName', [None])[0] 
            if jobId not in JobContainer:
                self.send_error(406, "Job Id '{}' has not been found".format(jobId)) #  Not Acceptable
                return 
            
            if JobContainer[jobId]['state'] not in ["READY","DONE"]:
                self.send_error(409   , "Job Id '{}' is already in {} state".format(jobId, JobContainer[jobId]['state'])) #  Conflict
                return 
            
            if JobContainer[jobId]['pid']:
                self.send_error(409   , "Job Id '{}' has already executiong task with pid: {}".format(JobContainer[jobId]['pid'])) #  Conflict
                return 
            

            testpath = JobContainer[jobId]['workDir']+"/tests/{}".format(testName)
            if not os.path.isdir(testpath):
                self.send_error(406, "The target directiry '{}' has not been found".format(testpath)) #  Not Acceptable
                return
            bfanpath = JobContainer[jobId]['workDir']+"/.bfan/bin/bfan.py"

            if not os.path.isfile(bfanpath):
                self.send_error(406, "The bfanpath pathh is invalid: '{}'".format(bfanpath)) #  Not Acceptable
                return
            pid,stdoutQueue = cmdExecutor.shellCmd("{} run --view jsonSummary {}".format(bfanpath, testpath), jobId, transcriptFunction, env=None, timeout=3*60*60)
            JobContainer[jobId]['pid'] = pid
            JobContainer[jobId]['stdoutQueue']=stdoutQueue
            JobContainer[jobId]['returnCode']=None
            JobContainer[jobId]['state']="RUNNING"


            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            responce = JobContainer[jobId].copy()
            del responce['stdoutQueue']
            self.wfile.write(json.dumps(responce).encode('utf-8'))
        elif path == '/jobs':
            self.clenup()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            responce = []
            for item in JobContainer.to_dict():
                item_cpy = JobContainer[item].copy()
                del item_cpy['stdoutQueue']
                responce.append(item_cpy)

            self.wfile.write(json.dumps(responce).encode('utf-8'))
        elif path == '/jobId':
            self.clenup()
            # Get server IP
            client_ip = self.client_address[0]
            existingJobId = findJobById(client_ip)
            jobId = existingJobId
            if not existingJobId:
                if len(JobContainer) != 0:
                   self.send_error(409, "Server rich Jobs limit {}".format(len(JobContainer))) # Conflict
                   return
                JobCounter = JobCounter + 1 
                jobId=str(JobCounter)

                if jobId in JobContainer:
                    self.send_error(500  , "Unable to register jobid={}".format(existingJobId)) # Internal Server Error
                    return
                JobContainer[jobId] = {'WDTimeout':False,'stdoutQueue':None,'returnCode':None, 'pid':None,'jobId':jobId,'IP':client_ip, 'user':os.getlogin(), 'refreshTime': time.time(), 'state':"READY",'workDir':"{}/bfun_{}".format(WORK_DIR,client_ip)}
                self.refresh(jobId)

            responce = JobContainer[jobId].copy()
            del responce['stdoutQueue']

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(responce).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")
            return
    
    def do_POST(self):
        self.updateProcessReturnCode()
        client_ip = self.client_address[0]
        if self.path == '/alive':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            message = post_data.decode('utf-8')
            
            # Log the message
            logging.info(f'Received message: {message}')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'logged'}).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")




if __name__ == '__main__':


    server_address = ('', 8080)  # Listen on all available interfaces, port 8080
    httpd = http.server.HTTPServer(server_address, CustomHandler)
    print("Server running on port 8080...")
    httpd.serve_forever()

    q.put("stop")
    hThread.join()
    

# curl localhost:8080/jobId
# curl "localhost:8080/startJob?jobId=2&testName=asasd"
# curl "localhost:8080/jobs"
# curl "localhost:8080/startJob?jobId=2&testName=envSetup.btest"
