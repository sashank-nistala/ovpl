import boto.ec2
import os

class CreateAwsVM:
        
    region = "us-east-1"
    conn_config = { "aws_access_key_id":"", 
            "aws_secret_access_key":""
            }
        
    def __init__(self):
        self.connection = self.create_connection()

    def create_connection(self):
        return boto.ec2.connect_to_region(self.region, **(self.conn_config))

    def get_few_fields(self, instance):
        dict = {'name':'', 'public-ip':'', 'private-ip':'', 'state':'', 'type':'', 'image-id':'', 'vpc-id':''}
        dict['name'] = instance.tags['Name']
        dict['public-ip'] = instance.ip_address
        dict['private-ip'] = instance.private_ip_address
        dict['state'] = instance.state
        dict['type'] = instance.instance_type
        dict['image-id'] = instance.image_id
        dict['vpc-id'] = instance.vpc_id
        return dict
    
    def get_all_instances(self, filter = None):
        instance_list = []
        reservations = self.connection.get_all_reservations(filters=filter)
        
        for reservation in reservations:
            for instance in reservation.instances:
                instance_list.append(instance)
            
        return instance_list
    
    def create_instance(self):
        reservation = self.connection.run_instances('ami-48400720', min_count=1, max_count=1,
                                    key_name="LabsKey-ver2", instance_type='t2.micro',
                                    subnet_id='subnet-587dc501', security_group_ids=['sg-524bc636'])
        reservation.instances[0].add_tag('Name', 'test.aws.adapter')
        return create_dictionary(reservation.instances[0])
    
    def stop_instances(self, filter=None):
        instances = self.get_all_instances(filter)
        instance_ids = []
        for instance in instances:
            instance_ids.append(instance.id)
        instances_stopped = self.connection.stop_instances(instance_ids)
        return instances_stopped

    def terminate_instances(self, filter=None):
        instances = self.get_all_instances(filter)
        running_instances = []
        for instance in instances:
            if instance.state not in ('terminated'):
                running_instances.append(instance)
        instance_ids = []
        for instance in running_instances:
            if(instance.get_attribute('disableApiTermination')['disableApiTermination']):
                instance.modify_attribute('disableApiTermination', 'False')
            instance_ids.append(instance.id)

        instances_terminated = self.connection.terminate_instances(instance_ids)
        return instances_terminated
    
if __name__ == '__main__':
#    os.environ['http_proxy']  = "http://proxy.iiit.ac.in:8080"
#    os.environ['https_proxy'] = "http://proxy.iiit.ac.in:8080"
    c = CreateAwsVM()
    filter1 = {'image_id':'ami-044d106c'}
#    list = map(c.get_few_fields, c.get_all_instances())
#    print list
#    print "number of instances = %d" % (list.__len__())

    print c.terminate_instances()
#    print create_instance()
#    print c.stop_instances(filter)
    
                             
