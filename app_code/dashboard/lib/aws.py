import boto3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

class AWS:

    def __init__(self):
        self.session = boto3.session.Session(
            aws_access_key_id='',
            aws_secret_access_key='',
            region_name='us-east-1'
        )

    def get_aws_storage(self):
        ce_client = self.session.client('ce')

        # The values are from two days ago
        two_days_before = datetime.utcnow() - timedelta(days=2)
        start_date = two_days_before.strftime('%Y-%m-%d')
        # End date
        end_date = datetime.utcnow() - timedelta(days=1)
        end_date = end_date.strftime('%Y-%m-%d')

        # Calculates days in the month
        day_one = two_days_before.replace(day=1)
        next_month = two_days_before.replace(day=28) + timedelta(days=4)
        next_month_day_one = next_month.replace(day=1)
        days_in_a_month = (next_month_day_one - day_one).days

        response_ebs = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='DAILY',
                                                   Filter={'Dimensions': {'Key': 'USAGE_TYPE_GROUP', 'Values': ['EC2: EBS - SSD(gp2)', 'EC2: EBS - Magnetic']}},
                                                   Metrics=['UsageQuantity'])

        response_s3 = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='DAILY',
                                                   Filter={'Dimensions': {'Key': 'USAGE_TYPE_GROUP', 'Values': ['S3: Storage - Standard']}},
                                                   Metrics=['UsageQuantity'])
        # The values for snapshots are taking many days to be updated
        # Get values from three days ago
        four_days_before = datetime.utcnow() - timedelta(days=4)
        start_date = four_days_before.strftime('%Y-%m-%d')
        # End date
        end_date = datetime.utcnow() - timedelta(days=3)
        end_date = end_date.strftime('%Y-%m-%d')
        response_snapshots = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='DAILY',
                                                          Filter={'Dimensions': {'Key': 'USAGE_TYPE_GROUP','Values': ['EC2: EBS - Snapshots']}},
                                                          Metrics=['UsageQuantity'])
        values = []
        for result in response_ebs['ResultsByTime']:
            if result['Total']:
                values.append(round(float(result['Total']['UsageQuantity']['Amount']) * days_in_a_month))
        for result in response_snapshots['ResultsByTime']:
            if result['Total']:
                values.append(round(float(result['Total']['UsageQuantity']['Amount']) * days_in_a_month))
        for result in response_s3['ResultsByTime']:
            if result['Total']:
                values.append(round(float(result['Total']['UsageQuantity']['Amount']) * days_in_a_month))

        results = {'values': values}
        return results

    def get_aws_storage_monthly(self):
        ce_client = self.session.client('ce')

        # Get last day of the last month
        last_month_day = datetime.utcnow().replace(day=1) - timedelta(days=1)
        end_date = last_month_day.strftime('%Y-%m-%d')
        
        start_date = (datetime.utcnow() + relativedelta(months=-6)).replace(day=1)
        start_date = start_date.strftime('%Y-%m-%d')

        response_ebs = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                    Filter={'Dimensions': {'Key': 'USAGE_TYPE_GROUP', 'Values': ['EC2: EBS - SSD(gp2)', 'EC2: EBS - Magnetic']}},
                                                    Metrics=['UsageQuantity'])

        response_snapshots = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                          Filter={'Dimensions': {'Key': 'USAGE_TYPE_GROUP', 'Values': ['EC2: EBS - Snapshots']}},
                                                          Metrics=['UsageQuantity'])

        response_s3 = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                   Filter={'Dimensions': {'Key': 'USAGE_TYPE_GROUP', 'Values': ['S3: Storage - Standard']}},
                                                   Metrics=['UsageQuantity'])

        months = []
        ebs_values = []

        for result in response_ebs['ResultsByTime']:
            start_date = result['TimePeriod']['Start']
            value = result['Total']['UsageQuantity']['Amount']
            date = datetime.strptime(start_date, "%Y-%m-%d")
            months.append(date.strftime('%b') + ' ' + date.strftime('%Y'))
            ebs_values.append(round(float(value)))

        snapshots_values = []
        for result in response_snapshots['ResultsByTime']:
            value = result['Total']['UsageQuantity']['Amount']
            snapshots_values.append(round(float(value)))

        s3_values = []
        for result in response_s3['ResultsByTime']:
            value = result['Total']['UsageQuantity']['Amount']
            s3_values.append(round(float(value)))

        results = {'months': months, 'ebs_values': ebs_values, 'snapshots_values': snapshots_values, 's3_values': s3_values}
        return results

    def get_aws_monthly_costs(self):
        ce_client = self.session.client('ce')

        # Get first day of the month
        # Use the firs day instead of the last day of the last month because otherwise it
        # does not count the last day
        first_day_month = datetime.utcnow().replace(day=1)
        end_date = first_day_month.strftime('%Y-%m-%d')
        # Replace the start day after 2018 is over. Only get last 12 month for example after that
        #start_date = '2018-01-01'
        start_date = (datetime.utcnow() + relativedelta(months=-6)).replace(day=1)
        start_date = start_date.strftime('%Y-%m-%d')

        ec2_response = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                    Filter={'Dimensions': {'Key': 'SERVICE', 'Values': ['Amazon Elastic Compute Cloud - Compute']}},
                                                    Metrics=['UnblendedCost'])

        rds_response = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                    Filter={'Dimensions': {'Key': 'SERVICE', 'Values': ['Amazon Relational Database Service']}},
                                                    Metrics=['UnblendedCost'])

        support_response = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                        Filter={'Dimensions': {'Key': 'SERVICE', 'Values': ['AWS Support (Business)']}},
                                                        Metrics=['UnblendedCost'])

        direct_connect_response = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                              Filter={'Dimensions': {'Key': 'SERVICE', 'Values': ['AWS Direct Connect']}},
                                                              Metrics=['UnblendedCost'])

        eks_response = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                         Filter={'Dimensions': {'Key': 'SERVICE', 'Values': ['Amazon Elastic Container Service for Kubernetes']}},
                                                         Metrics=['UnblendedCost'])

        vpc_response = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                    Filter={'Dimensions': {'Key': 'SERVICE', 'Values': ['Amazon Virtual Private Cloud']}},
                                                    Metrics=['UnblendedCost'])

        ec2_other_response = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                          Filter={'Dimensions': {'Key': 'SERVICE', 'Values': ['EC2 - Other']}},
                                                          Metrics=['UnblendedCost'])

        others_response = ce_client.get_cost_and_usage(TimePeriod={'Start': start_date, 'End': end_date}, Granularity='MONTHLY',
                                                       Filter={'Dimensions': {'Key': 'SERVICE', 'Values': ['AWS Budgets',
                                                                'AWS CloudTrail', 'AWS Config', 'AWS Directory Service',
                                                                'AWS IoT', 'AWS Key Management Service', 'AWS Lambda',
                                                                'Amazon Elastic File System', 'Amazon Elastic Load Balancing',
                                                                'Amazon Elasticsearch Service', 'Amazon GuardDuty',
                                                                'Amazon Simple Notification Service', 'Amazon Simple Queue Service',
                                                                'Amazon Redshift', 'Amazon EC2 Container Service',
                                                                'Amazon Simple Storage Service', 'Amazon WorkDocs', 'AmazonCloudWatch']}},
                                                       Metrics=['UnblendedCost'])

        months = []
        ec2_values = []
        for result in ec2_response['ResultsByTime']:
            start_date = result['TimePeriod']['Start']
            value = result['Total']['UnblendedCost']['Amount']

            date = datetime.strptime(start_date, "%Y-%m-%d")
            months.append(date.strftime('%b') + ' ' + date.strftime('%Y'))
            ec2_values.append(round(float(value), 2))

        rds_values = []
        for result in rds_response['ResultsByTime']:
            value = result['Total']['UnblendedCost']['Amount']
            rds_values.append(round(float(value), 2))

        support_values = []
        for result in support_response['ResultsByTime']:
            value = result['Total']['UnblendedCost']['Amount']
            support_values.append(round(float(value), 2))

        direct_connect_values = []
        for result in direct_connect_response['ResultsByTime']:
            value = result['Total']['UnblendedCost']['Amount']
            direct_connect_values.append(round(float(value), 2))

        eks_values = []
        for result in eks_response['ResultsByTime']:
            value = result['Total']['UnblendedCost']['Amount']
            eks_values.append(round(float(value), 2))

        vpc_values = []
        for result in vpc_response['ResultsByTime']:
            value = result['Total']['UnblendedCost']['Amount']
            vpc_values.append(round(float(value), 2))

        ec2_other_values = []
        for result in ec2_other_response['ResultsByTime']:
            value = result['Total']['UnblendedCost']['Amount']
            ec2_other_values.append(round(float(value), 2))

        others_values = []
        for result in others_response['ResultsByTime']:
            value = result['Total']['UnblendedCost']['Amount']
            others_values.append(round(float(value), 2))

        # Get total costs for each month
        months_totals = []
        for i in range(len(months)):
            total = ec2_values[i] + rds_values[i] + support_values[i] + direct_connect_values[i] + eks_values[i] + vpc_values[i] +ec2_other_values[i] + others_values[i]
            months_totals.append(round(total, 2))

        results = {'months': months, 'ec2_values': ec2_values, 'rds_values': rds_values, 'support_values': support_values,
                   'direct_connect_values': direct_connect_values, 'eks_values': eks_values, 'vpc_values': vpc_values,
                   'ec2_other_values': ec2_other_values, 'others_values': others_values, 'months_totals': months_totals}
        return results
