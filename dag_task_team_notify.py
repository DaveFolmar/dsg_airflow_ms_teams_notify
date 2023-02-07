
from ms_teams_webhook_operator import MSTeamsWebhookOperator
from ms_teams_webhook_hook import MSTeamsWebhookHook
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pytz

def convert_datetime(datetime_string):
    return datetime_string.astimezone(pytz.timezone('America/New_York')).strftime('%b-%d %H:%M:%S')


def dag_triggered_callback(context):
    log_url = context.get("task_instance").log_url
    teams_msg = f"""
            DAG has been triggered.
            Task: {context.get('task_instance').task_id}  
            DAG: {context.get('task_instance').dag_id} 
            Execution Time: {convert_datetime(context.get('execution_date'))}
            """
    teams_notification = MSTeamsWebhookOperator(
        task_id="ms_teams_callback",
        trigger_rule="all_done",
        message=teams_msg,
        button_text="View log",
        button_url=log_url,
        button2_text="SOP",
        button2_url="https://confluence.dcsg.com/display/WA/Astronomer+Airflow+SOP",
        theme_color="FF0000",
        http_conn_id="ms_teams_callbacks",
    )
    return teams_notification.execute(context)


def dag_success_callback(context):
    log_url = context.get("task_instance").log_url
    teams_msg = f"""
            DAG has succeeded.
            Task: {context.get('task_instance').task_id}  
            DAG: {context.get('task_instance').dag_id} 
            Execution Time: {context.get('execution_date')}  
            """
    teams_notification = MSTeamsWebhookOperator(
        task_id="ms_teams_callback",
        trigger_rule="all_done",
        message=teams_msg,
        button_text="View log",
        button_url=log_url,
        button2_text="SOP",
        button2_url="https://confluence.dcsg.com/display/WA/Astronomer+Airflow+SOP",
        theme_color="FF0000",
        http_conn_id="ms_teams_callbacks",
    )
    return teams_notification.execute(context)

def success_callback(context):
    log_url = context.get("task_instance").log_url
    local_time = {convert_datetime(context.get('execution_date'))}
    teams_msg = f"""
            Task has succeeded. 
            Task: {context.get('task_instance').task_id}  
            DAG: {context.get('task_instance').dag_id} 
            Execution Time: {convert_datetime(context.get('execution_date'))}
            """
    teams_notification = MSTeamsWebhookOperator(
        task_id="ms_teams_callback",
        trigger_rule="all_done",
        message=teams_msg,
        button_text="View log",
        button_url=log_url,
        button2_text="SOP",
        button2_url="https://confluence.dcsg.com/display/WA/Astronomer+Airflow+SOP",
        theme_color="2E8B57",
        http_conn_id="ms_teams_callbacks",
    )
    return teams_notification.execute(context)

def failure_callback(context):
    log_url = context.get("task_instance").log_url
    teams_msg = f"""
            Task has Failed. 
            Task: {context.get('task_instance').task_id}  
            DAG: {context.get('task_instance').dag_id} 
            Execution Time: {convert_datetime(context.get('execution_date'))}
            """
    teams_notification = MSTeamsWebhookOperator(
        task_id="ms_teams_callback",
        trigger_rule="all_done",
        message=teams_msg,
        button_text="View log",
        button_url=log_url,
        button2_text="SOP",
        button2_url="https://confluence.dcsg.com/display/WA/Astronomer+Airflow+SOP",
        theme_color="FF0000",
        http_conn_id="ms_teams_callbacks",
    )
    return teams_notification.execute(context)

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis, *args, **kwargs):
    dag_id = slas[0].dag_id
    task_id = slas[0].task_id
    execution_date = slas[0].execution_date.isoformat()
    teams_msg = f"""
            SLA has been missed.
            Task: {task_id}  
            DAG: {dag_id} 
            Execution Time: {convert_datetime(context.get('execution_date'))}
            """
    hook = MSTeamsWebhookHook(
        message=teams_msg,
        theme_color="FF0000",
        http_conn_id='ms_teams_callbacks')
    hook.execute()

def _start():
    pass
# Force a failure in this task - for demo - will trigger a failed trigger
def _end():

    exit(2)

default_args = {
    'owner': 'Folmar',
    'start_date': datetime(2022, 11, 27),
    'email': ['dave.folmar@dcsg.com'],
    'email_on_failure': False,
    'on_failure_callback': failure_callback,
    'on_success_callback': success_callback
}

with DAG('dag_task_team_notify', default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:

    start = PythonOperator(
        task_id='start',
        python_callable=_start
    )
    end = PythonOperator(
        task_id='end',
        python_callable=_end
    )

    # Below - defines the flow - start then end, if stated as start << end  - then end would be executed first.
    start >> end

