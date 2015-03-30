import requests
import json
from adapters.VMUtils import convert_to_megs

status=[]
status.append("Deploy request received")
status.append("VM created")
status.append("Installing Dependencies")
status.append("Lab deploy successful!")
lab_id_deployed=0 #global variable to update status at reqd. checkpoints

def post_labs(lab_spec):
	lab_loader={
	'lab_id':lab_spec['lab_id'],
	'slug':lab_spec['lab']['description']['slug'],
	'institute_id':lab_spec['lab']['description']['institute']['id'],
	'discipline_id':lab_spec['lab']['description']['discipline']['id'],
	'name':lab_spec['lab']['description']['name'],
	'type_of_lab':lab_spec['lab']['description']['type'],
	'integration_level':lab_spec['lab']['description']['integration_level'],
	'is_src_avail':True,
	'is_content_avail':True,
	'status':status[0]
	}
	lab=requests.post("http://localhost:5000/labs",data=lab_loader)
	if (lab.status_code != 200):
		print "Error in POSTing to labs table"
	else:
		return lab.json()['id']
		 
def post_labsysteminfo(lab_spec,lab_id):
	min=lab_spec['lab']['runtime_requirements']['platform']['storage']['min_required']	
	storage=convert_to_megs(min)
	mem=lab_spec['lab']['runtime_requirements']['platform']['memory']['min_required']
	memory=convert_to_megs(mem)
	labsysteminfo_loader={
	'lab_id':lab_id,
	'os':lab_spec['lab']['runtime_requirements']['platform']['os'],
	'storage':storage,
	'os_version':lab_spec['lab']['runtime_requirements']['platform']['osVersion'],
	'memory': memory,	
	'hosting':lab_spec['lab']['runtime_requirements']['platform']['hosting'],
	'architecture':lab_spec['lab']['runtime_requirements']['platform']['arch']
	}
	labsysteminfo=requests.post("http://localhost:5000/labsysteminfo",data=labsysteminfo_loader)
	labsysteminfo_id=labsysteminfo.json()['id']	
	if (labsysteminfo.status_code != 200):
		print "Error in POSTing to lab_system_info table"
	else:
		return labsysteminfo_id

def put_labsysteminfo(labsysteminfo_id,vm_id,vm_ip):
	#update labsysteminfo table with vm_ip,vm_id
	labsysteminfo_up={'vm_id':str(vm_id),'ipaddress':str(vm_ip)}
	labsysteminfo=requests.put("http://localhost:5000/labsysteminfo/"+str(labsysteminfo_id),data=labsysteminfo_up)
		
def put_labs(lab_spec,lab_id):
	#update labs table with repo_url and new status	
	l_up={'status':status[1],'repo_url':lab_spec['lab_src_url'],'is_deployed':True}
	lab=requests.put("http://localhost:5000/labs/"+str(lab_id),data=l_up) 	

def update_status(lab_id,i):
	data={"status":status[i]}	
	lab_update=requests.put("http://localhost:5000/labs/"+str(lab_id),data=data) 	
