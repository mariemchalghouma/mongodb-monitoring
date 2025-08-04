import yaml
import smtplib
from datetime import datetime 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from typing import Dict , List , Any , Optional 

class AlertManager :
    def load_config(path="C:/Users/Admin/Desktop/mongodb_monitoring/config.yaml") :
            with open (path , 'r') as file :
                return yaml.safe_load(file)
    def __init__(self,config) :
         self.config=config
         self.thresholds=config['alerts']['threshold']
         self.active_alerts={}

    def ckeck_threholds(self, metrics) -> List[Dict[str,Any]]:
         alerts=[]
         for metric_name, metric_value in metrics.items():
              if metric_name in ['time', 'query_performance']:
                   continue
              if metric_name in self.thresholds:
                   threshold_config=self.thresholds['metric_name']
                   alert=self._evaluate_threshold(metric_name, metric_value, threshold_config)
                   if alert :
                        alerts.append(alert)
         if 'query_performance' in metrics  and 'query_performance' in self.thresholds :
              qp_alerts=self._ckeck_query_performance(metrics['query_performance'])
              alerts.extend(qp_alerts)
         return alerts 
    


    def _evaluate_threshold (self, metric_name , metric_valeur , threshold_config) :
         if metric_valeur is None :
              return None
         alert_triggered=False 
         severity='info'
         message=""

         if 'critical' in threshold_config and metric_valeur>= threshold_config['critical'] :
              alert_triggered=True
              severity='critical'
              message=f"{metric_name} is critical : {metric_valeur} > {threshold_config["critical"]}"
         elif 'warning'in threshold_config and metric_valeur>= threshold_config['warning']  :
              alert_triggered=True
              severity='warning'
              message=f"{metric_name} is warning : {metric_valeur} > {threshold_config["warning"]}"
         if alert_triggered :
              return
              {
                   'metric': metric_name,
                   'value': metric_valeur,
                   'severity' :severity ,
                   'message' : message ,
                   'time': datetime.now().isoformat() ,
                   'threshold_exceeded': threshold_config.get(severity,0)

              }
         return  None 
    



    def _ckeck_query_performance(self, query_performance):
         alert=[]
         qp_threshols=self.thresholds['query_performance']
         for operation , count in query_performance.items():
              if operation in qp_threshols :
                   threshold_config=qp_threshols[operation]
                   alert=self._evaluate_threshold(f"query{operation}", count , threshold_config)
         if alert :
              return alert 
    def _create_email_body(self, alerts, severity) :
         for alert in alerts:
            html += f"""
            <html>
             <body>
                <tr>
                    <td>{alert['metric']}</td>
                    <td>{alert['value']}</td>
                    <td>{alert['threshold_exceeded']}</td>
                    <td>{alert['message']}</td>
                </tr>
             </body>
            </html>
            """
            return html 
    def _send_email_alert(self, alerts , severity) :
         email_config=self.thresholds.get('alerts' , {}).get('email',{})
         msg=MIMEMultipart()
         msg['from']=email_config['from_email']
         msg['To']=', '.join(email_config['to_emails'])
         msg['Subject'] = f"MongoDB Alert - {severity.upper()}"
         body=self._create_email_body(self,alerts, severity)
         msg.attach(MIMEText(body, 'html'))
         server=smtplib.SMTP(email_config['smtp_server'] , email_config['smtp_port'])
         if email_config.get('use_tls', True) :
              server.starttls()
         if 'username' in email_config and 'password' in email_config :
              server.login(email_config['username'] , email_config['password'])
         server.sendmail(email_config['from_email'], email_config['to_emails'], msg.as_string())
    
         





 


              

                    
        
              


