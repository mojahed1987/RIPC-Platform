import requests
import pandas as pd
import json
import os
import arcpy
from datetime import datetime

# =========================
#  TOKEN
# =========================
TOKEN = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIyMzg2MjczMTg1Iiwicm9sZSI6WyJTVVBFUlZJU09SX1VTRVIiLCJGWVFCUVdNUlhXIiwiU0JZSUtWV0hJRSIsIlJaSk5KSU1JVlIiLCJDWk1SQ1dPTVNUIiwiVlJXQ0lKSklHTCIsIllURVhOSlhEUUQiLCJNQVNURVJfUExBTl9WSUVXRVIiLCJUTUlVSVdYSURTIiwiVFJBRkZJQ19BQ0NJREVOVF9SRVBPUlRFUiIsIlRWRUxXSklMT1oiLCJJU05PSkpSQlhCIl0sImF1dGhvcml0aWVzIjoiUk9MRV9TVVBFUlZJU09SX1VTRVIsQVBQTElDQVRJT05fcXVhbGlmaWNhdGlvbnMsTU9EVUxFX3N1cGVydmlzb3ItdXNlci1xdWFsaWZpY2F0aW9ucyxNT0RVTEVfY2VydGlmaWNhdGVzLXF1YWxpZmljYXRpb25zLEFQUExJQ0FUSU9OX3BsYW5uaW5nLE1PRFVMRV9wYXJ0bmVyLXVzZXItcGxhbm5pbmcsQVBQTElDQVRJT05fcGVybWl0cyxNT0RVTEVfcGVybWl0LXJlcXVlc3QtbW9kdWxlLE1PRFVMRV9wZXJtaXQtbW9kdWxlLE1PRFVMRV9jb29yZGluYXRpb24tbW9kdWxlLE1PRFVMRV9ibG9ja2luZy1tb2R1bGUsTU9EVUxFX3VuYmxvY2tpbmctbW9kdWxlLE1PRFVMRV9wZXJtaXQtbWFuYWdlbWVudC1tb2R1bGUsTU9EVUxFX3JlZ3VsYXJpdHktcGFydG5lci1zZXJ2aWNlLXByb3ZpZGVyLXYxLXBlcm1pdC1yZXF1ZXN0LW1hbmFnZW1lbnQtbW9kdWxlLE1PRFVMRV9yZWd1bGFyaXR5LXBhcnRuZXItc2VydmljZS1wcm92aWRlci12MS1wZXJtaXQtbWFuYWdlbWVudC1tb2R1bGUsTU9EVUxFX3JlZ3VsYXJpdHktcGFydG5lci1zZXJ2aWNlLXByb3ZpZGVyLXYxLXBlcm1pdC1tYW5hZ2VtZW50LXJlcXVlc3QtbW9kdWxlLE1PRFVMRV9yZWd1bGFyaXR5LXBhcnRuZXItc2VydmljZS1wcm92aWRlci12Mi1wZXJtaXQtcmVxdWVzdC1tYW5hZ2VtZW50LW1vZHVsZSxNT0RVTEVfcmVndWxhcml0eS1wYXJ0bmVyLXNlcnZpY2UtcHJvdmlkZXItdjItcGVybWl0LW1hbmFnZW1lbnQtbW9kdWxlLE1PRFVMRV9yZWd1bGFyaXR5LXBhcnRuZXItc2VydmljZS1wcm92aWRlci12Mi1wZXJtaXQtbWFuYWdlbWVudC1yZXF1ZXN0LW1vZHVsZSxNT0RVTEVfcmVndWxhcml0eS1wYXJ0bmVyLXNlcnZpY2UtcHJvdmlkZXItcmVzdHJpY3Rpb24tcmVxdWVzdC1tYW5hZ2VtZW50LW1vZHVsZSxNT0RVTEVfcmVndWxhcml0eS1wYXJ0bmVyLXNlcnZpY2UtcHJvdmlkZXItcmVzdHJpY3Rpb24tbWFuYWdlbWVudC1tb2R1bGUsTU9EVUxFX3JlZ3VsYXJpdHktcGFydG5lci1zZXJ2aWNlLXByb3ZpZGVyLWJsb2NraW5nLXJlcXVlc3QtbWFuYWdlbWVudC1tb2R1bGUsTU9EVUxFX3JlZ3VsYXJpdHktcGFydG5lci1zZXJ2aWNlLXByb3ZpZGVyLXVuYmxvY2tpbmctcmVxdWVzdC1tYW5hZ2VtZW50LW1vZHVsZSxNT0RVTEVfcmVndWxhcml0eS1wYXJ0bmVyLXNlcnZpY2UtcHJvdmlkZXItY29vcmRpbmF0aW9uLXJlcXVlc3QtbWFuYWdlbWVudC1tb2R1bGUsQVBQTElDQVRJT05fb2JqZWN0aW9uLE1PRFVMRV92aW9sYXRpb25zLXJlcG9ydHMsQVBQTElDQVRJT05fcGxhbm5pbmctdjMsTU9EVUxFX3BhcnRuZXItdXNlci1wbGFubmluZy1tb2R1bGUsTU9EVUxFX3BhcnRuZXItdXNlci1wcm9qZWN0cy1tYW5hZ2VtZW50LW1vZHVsZSxNT0RVTEVfcGFydG5lci11c2VyLWNoYW5nZS1yZXF1ZXN0LW1hbmFnZW1lbnQtbW9kdWxlLE1PRFVMRV9yZWd1bGF0b3J5LXBhcnRuZXItc2VydmljZS1wcm92aWRlcnMtcHJvamVjdHMtbWFuYWdlbWVudC1tb2R1bGUsTU9EVUxFX3JlZ3VsYXRvcnktcGFydG5lci1zZXJ2aWNlLXByb3ZpZGVycy1wcm9qZWN0LXJlcXVlc3QtbWFuYWdlbWVudC1tb2R1bGUsTU9EVUxFX3JlZ3VsYXRvcnktcGFydG5lci1zZXJ2aWNlLXByb3ZpZGVycy1jaGFuZ2UtcmVxdWVzdC1tYW5hZ2VtZW50LW1vZHVsZSxST0xFX0ZZUUJRV01SWFcsUk9MRV9TQllJS1ZXSElFLEFQUExJQ0FUSU9OX21haW5hcHAsTU9EVUxFX3N1cGVydmlzb3ItdXNlcnMtbWFuYWdlbWVudCxNT0RVTEVfbGlua2VkLXN1cGVydmlzb3ItcHJvZmlsZXMtbWFuYWdlbWVudCxNT0RVTEVfcGVybWl0cy1tb25pdG9ycyxBUFBMSUNBVElPTl9tYXN0ZXItcGxhbixNT0RVTEVfbWFzdGVyLXBsYW4tbGlua2VkLXBhcnRuZXItcHJvZmlsZXMtbW9kdWxlLEFQUExJQ0FUSU9OX2ludGVycnVwdGlvbnMsTU9EVUxFX2ludGVycnVwdGlvbnMsQVBQTElDQVRJT05fZW5jcm9hY2htZW50cyxNT0RVTEVfZW5jcm9hY2htZW50cyxBUFBMSUNBVElPTl90cmFmZmljLWFjY2lkZW50cyxNT0RVTEVfdHJhZmZpYy1hY2NpZGVudHMsQVBQTElDQVRJT05fZ2lnYS1wcm9qZWN0cyxNT0RVTEVfZ2lnYS1wcm9qZWN0cy1tb2R1bGUsUk9MRV9SWkpOSklNSVZSLFJPTEVfQ1pNUkNXT01TVCxST0xFX1ZSV0NJSkpJR0wsUk9MRV9ZVEVYTkpYRFFELFJPTEVfTUFTVEVSX1BMQU5fVklFV0VSLFJPTEVfVE1JVUlXWElEUyxST0xFX1RSQUZGSUNfQUNDSURFTlRfUkVQT1JURVIsUk9MRV9UVkVMV0pJTE9aLFJPTEVfSVNOT0pKUkJYQixyZWd1bGF0b3J5LXBhcnRuZXItYnJvd3NlLXNlcnZpY2UtcHJvdmlkZXJzLWNoYW5nZS1yZXF1ZXN0cyxyZWd1bGFyaXR5LXBhcnRuZXItYnJvd3NlLXYyLXBlcm1pdC1tYW5hZ2VtZW50LXJlcXVlc3RzLHJlZ3VsYXJpdHktcGFydG5lci1icm93c2UtcmVzdHJpY3Rpb25zLHBhcnRuZXItcHJvY2Vzcy1naWdhLXByb2plY3QtcmVxdWVzdCxwYXJ0bmVyLXJldHVybi1naWdhLXByb2plY3QtcmVxdWVzdCxtb2RpZnktcGFydG5lci1wcm9qZWN0LXJlcXVlc3QscmVndWxhdG9yeS1wYXJ0bmVyLWJyb3dzZS1zZXJ2aWNlLXByb3ZpZGVycy1wcm9qZWN0cyxicm93c2UtbXktdmlvbGF0aW9ucy1yZXBvcnRzLHJlZ3VsYXJpdHktcGFydG5lci1icm93c2UtY29vcmRpbmF0aW9uLXJlcXVlc3RzLHJlZ3VsYXRvcnktcGFydG5lci1icm93c2Utc2VydmljZS1wcm92aWRlcnMtcHJvamVjdC1yZXF1ZXN0cyxyZWd1bGF0b3J5LXBhcnRuZXItdmlldy1zZXJ2aWNlLXByb3ZpZGVyLWNoYW5nZS1yZXF1ZXN0LWRldGFpbHMscmVndWxhcml0eS1wYXJ0bmVyLXZpZXctcmVzdHJpY3Rpb24tcmVxdWVzdC1kZXRhaWxzLHJlZ3VsYXJpdHktcGFydG5lci1icm93c2UtYmxvY2tpbmctcmVxdWVzdHMsZWRpdC1jb29yZGluYXRlLXBlcm1pdC1yZXF1ZXN0LXBhcnRuZXIscmVndWxhdG9yeS1wYXJ0bmVyLWV4cG9ydC1zZXJ2aWNlLXByb3ZpZGVycy1jaGFuZ2UtcmVxdWVzdHMtdG8tZXhjZWwsYnJvd3NlLWxpbmtlZC1wcm9maWxlLWludGVycnVwdGlvbnMsdmlldy1wZXJtaXQtcmVxdWVzdC1kZXRhaWxzLXN1cGVydmlzb3IscmVndWxhcml0eS1wYXJ0bmVyLWJyb3dzZS12Mi1wZXJtaXRzLHJlZ3VsYXRvcnktcGFydG5lci1leHBvcnQtc2VydmljZS1wcm92aWRlcnMtcHJvamVjdC1yZXF1ZXN0cy10by1leGNlbCxkZS1saW5rLXN1cGVydmlzb3ItdXNlcixwYXJ0bmVyLXZpZXctZ2lnYS1wcm9qZWN0LWRldGFpbHMsdmlldy1saW5rZWQtcHJvZmlsZS1naXMtbWFwLHBhcnRuZXItY29uZmlybS1lbmNyb2FjaG1lbnQtcmVwb3J0LGJyb3dzZS1wYXJ0bmVyLXByb2plY3RzLXJlcXVlc3RzLHByb2Nlc3MtaW50ZXJydXB0aW9uLGJyb3dzZS1xdWFsaWZpY2F0aW9uLWNlcnRpZmljYXRlcyxwYXJ0bmVyLXJldHVybi1lbmNyb2FjaG1lbnQtcmVwb3J0LHVuc3VzcGVuZC1xdWFsaWZpY2F0aW9uLWNlcnRpZmljYXRlLHBhcnRuZXItYXBwcm92ZS1wcm9qZWN0LXJlcXVlc3QscmVndWxhcml0eS1wYXJ0bmVyLXZpZXctdjItcGVybWl0LWRldGFpbHMsdXBkYXRlLWJsb2NraW5nLXJlcXVlc3QscmVndWxhcml0eS1wYXJ0bmVyLWJyb3dzZS1wZXJtaXQtbWFuYWdlbWVudC1yZXF1ZXN0cyx2aWV3LXVuYmxvY2tpbmctcmVxdWVzdC1kZXRhaWxzLXBhcnRuZXIsdmlldy1saW5rZWQtcHJvZmlsZS1kYXNoYm9hcmQsdHJhZmZpYy1wYXJ0bmVyLXByb2Nlc3MtdG1wLXJlcXVlc3QsbW9kaWZ5LWVuY3JvYWNobWVudC1yZXBvcnQscGFydG5lci12aWV3LXByb2plY3QtcmVxdWVzdC1kZXRhaWxzLHBhcnRuZXItc3VibWl0LWNhbmNlbC1wcm9qZWN0LWNoYW5nZS1yZXF1ZXN0LHByaW50LXRyYWZmaWMtYWNjaWRlbnQtcmVwb3J0LHJlZ3VsYXJpdHktcGFydG5lci12aWV3LXJlc3RyaWN0aW9uLWRldGFpbHMscmVndWxhcml0eS1wYXJ0bmVyLXZpZXctcGVybWl0LXJlcXVlc3QtZGV0YWlscyx2aWV3LXBlcm1pdC1yZXF1ZXN0LXByb2plY3QtZGV0YWlscyxjcmVhdGUtYmxvY2tpbmctcmVxdWVzdCxjcmVhdGUtaW50ZXJydXB0aW9uLHJldHVybi1yZXBvcnQtdG8tcmlwYyxwYXJ0bmVyLXN1Ym1pdC1naWdhLXByb2plY3QtcmVwb3J0LHN1Ym1pdC1leHRlbmQtcGFydG5lci1wcm9qZWN0LXJlcXVlc3QscGFydG5lci1yZWplY3QtcHJvamVjdC1yZXF1ZXN0LHJlamVjdC1xdWFsaWZpY2F0aW9uLXJlcXVlc3QsYnJvd3NlLWxpbmtlZC1wcm9maWxlLXJlcG9ydHMscGFydG5lci1leHBvcnQtY2hhbmdlLXJlcXVlc3RzLXRvLWV4Y2VsLHJlZ3VsYXJpdHktcGFydG5lci12aWV3LXYyLXBlcm1pdC1tYW5hZ2VtZW50LXJlcXVlc3QtZGV0YWlscyxicm93c2UtcGVybWl0LXJlcXVlc3QtbGlzdC1zdXBlcnZpc29yLHZpZXctcGVybWl0LW1hbmFnZW1lbnQtcmVxdWVzdHMtcGFydG5lcixwYXJ0bmVyLWV4cG9ydC1wcm9qZWN0cy10by1leGNlbCxtb2RpZnktdHJhZmZpYy1hY2NpZGVudC1yZXBvcnQscmVndWxhcml0eS1wYXJ0bmVyLWJyb3dzZS1wZXJtaXQtcmVxdWVzdHMsdmlldy1xdWFsaWZpY2F0aW9uLWNlcnRpZmljYXRlLWRldGFpbHMscGFydG5lci1zdWJtaXQtcHJvamVjdC1yZXF1ZXN0LHJlZ3VsYXJpdHktcGFydG5lci12aWV3LXVuYmxvY2tpbmctcmVxdWVzdC1kZXRhaWxzLHZpZXctY29vcmRpbmF0ZS1yZXF1ZXN0LWRldGFpbHMtcGFydG5lcix2aWV3LXZpb2xhdGlvbi1kZXRhaWxzLGFwcHJvdmUtdW5ibG9ja2luZy1yZXF1ZXN0LWRlY2lzaW9uLXN1cGVydmlzb3Iscm9hZC1vd25lci1wcm9jZXNzLXRtcC1yZXF1ZXN0LHRyYW5zZmVyLWVuY3JvYWNobWVudC1yZXBvcnQsY29vcmRpbmF0ZS13aXRoLW5vdGUtcGFydG5lcixyZWd1bGFyaXR5LXBhcnRuZXItYnJvd3NlLXBlcm1pdHMscmVqZWN0LXVuYmxvY2tpbmctcmVxdWVzdC1kZWNpc2lvbi1zdXBlcnZpc29yLHVwZGF0ZS1saW5rZWQtc3VwZXJ2aXNvci1wcm9maWxlLGJyb3dzZS1wZXJtaXQtbGlzdC1tb25pdG9yLGFjY2VwdC1jbG9zdXJlLXBlcm1pdC1yZXF1ZXN0LWRlY2lzaW9uLXN1cGVydmlzb3IscmVndWxhcml0eS1wYXJ0bmVyLXZpZXctcGVybWl0LWRldGFpbHMsdmlldy1saW5rZWQtcHJvZmlsZS1nYW50dC1jaGFydCxyZWd1bGFyaXR5LXBhcnRuZXItYnJvd3NlLXVuYmxvY2tpbmctcmVxdWVzdHMsdmlldy1wYXJ0bmVyLXByb2plY3QtcmVxdWVzdC1kZXRhaWxzLHZpZXctc3VwZXJ2aXNvci1xdWFsaWZpY2F0aW9uLXJlcXVlc3QtZGV0YWlscyxyZWd1bGF0b3J5LXBhcnRuZXItdmlldy1zZXJ2aWNlLXByb3ZpZGVyLXByb2plY3QtZGV0YWlscyx2aWV3LWNsb3N1cmUtcGVybWl0LXJlcXVlc3QtZGV0YWlscy1zdXBlcnZpc29yLHZpZXctc3VwZXJ2aXNvci11c2VyLGJyb3dzZS11bmJsb2NraW5nLXJlcXVlc3QtbGlzdC1wYXJ0bmVyLHJlZ3VsYXJpdHktcGFydG5lci12aWV3LWNvb3JkaW5hdGlvbi1yZXF1ZXN0LWRldGFpbHMsYnJvd3NlLXN1cGVydmlzb3ItdXNlcnMsdXBkYXRlLXN1cGVydmlzb3ItdXNlcixjYW5jZWwtaW50ZXJydXB0aW9uLGFjY2VwdC1xdWFsaWZpY2F0aW9uLXJlcXVlc3Qsdmlldy1wZXJtaXQtcmVxdWVzdC1hY3RpdmUtcHJvamVjdHMscGFydG5lci1hZGQtcHJvamVjdC10ZWFtLGFjdGl2YXRlLWRlYWN0aXZhdGUtc3VwZXJ2aXNvci11c2VyLGJyb3dzZXItY29vcmRpbmF0aW9uLWxpc3QtcGFydG5lcixyZWd1bGFyaXR5LXBhcnRuZXItYnJvd3NlLXJlc3RyaWN0aW9uLXJlcXVlc3RzLHBhcnRuZXItdmlldy1jaGFuZ2UtcmVxdWVzdC1kZXRhaWxzLHJlamVjdC1jbG9zdXJlLXBlcm1pdC1yZXF1ZXN0LWRlY2lzaW9uLXN1cGVydmlzb3IsYnJvd3NlLWJsb2NraW5nLXJlcXVlc3QtbGlzdC1wYXJ0bmVyLHJlZ3VsYXRvcnktcGFydG5lci1leHBvcnQtc2VydmljZS1wcm92aWRlcnMtcHJvamVjdHMtdG8tZXhjZWwscHJvY2Vzcy10cmFmZmljLWFjY2lkZW50LXJlcG9ydCx2aWV3LWxpbmtlZC1wcm9maWxlLWxpc3QscGFydG5lci1jYW5jZWwtcHJvamVjdC1yZXF1ZXN0LHBhcnRuZXItYnJvd3NlLXByb2plY3QscmVndWxhdG9yeS1wYXJ0bmVyLXZpZXctc2VydmljZS1wcm92aWRlci1wcm9qZWN0LXJlcXVlc3QtZGV0YWlscyxzdWJtaXQtcGFydG5lci1wcm9qZWN0LXJlcXVlc3Qsdmlldy1pbnRlcnJ1cHRpb24tZGV0YWlscyxzdXNwZW5kLXF1YWxpZmljYXRpb24tY2VydGlmaWNhdGUsYnJvd3NlLXBhcnRuZXItcHJvamVjdHMscHJvY2Vzcy1lbmNyb2FjaG1lbnQtcmVwb3J0LHBhcnRuZXItdmlldy1lbmNyb2FjaG1lbnQtcmVwb3J0LWRldGFpbHMsdmlldy1leHRlbmQtcGVybWl0LXJlcXVlc3RzLWRldGFpbHMtcGFydG5lcixwYXJ0bmVyLW1vZGlmeS1wcm9qZWN0LXJlcXVlc3Qsdmlldy1wZXJtaXQtdG90YWwtZmVlcyxwYXJ0bmVyLWJyb3dzZS1jaGFuZ2UtcmVxdWVzdCx2aWV3LWJsb2NraW5nLXJlcXVlc3QtZGV0YWlscy1wYXJ0bmVyLHRha2UtcGVybWl0LXJlcXVlc3QtZGVjaXNpb24tc3VwZXJ2aXNvcixyZWd1bGFyaXR5LXBhcnRuZXItdmlldy1wZXJtaXQtbWFuYWdlbWVudC1yZXF1ZXN0LWRldGFpbHMsY3JlYXRlLWVuY3JvYWNobWVudC1yZXBvcnQscGFydG5lci1icm93c2UtcHJvamVjdC1yZXF1ZXN0LHZpZXctdHJhZmZpYy1hY2NpZGVudC1yZXBvcnQtZGV0YWlscyxicm93c2Utc3VwZXJ2aXNvci1xdWFsaWZpY2F0aW9uLXJlcXVlc3RzLGNyZWF0ZS10cmFmZmljLWFjY2lkZW50LXJlcG9ydCxwYXJ0bmVyLXN1Ym1pdC1lZGl0LXByb2plY3QtY2hhbmdlLXJlcXVlc3QsY2FuY2VsLWJsb2NraW5nLXJlcXVlc3Qsc3VibWl0LWVkaXQtcHJvamVjdC1yZXF1ZXN0LHJlZ3VsYXJpdHktcGFydG5lci12aWV3LXYyLXBlcm1pdC1yZXF1ZXN0LWRldGFpbHMsdmlldy1wYXJ0bmVyLXByb2plY3QtZGV0YWlscyxjcmVhdGUtc3VwZXJ2aXNvci11c2VyLGJyb3dzZS1wcm9qZWN0cy1wZXJtaXRzLXZpb2xhdGlvbnMtcmVwb3J0cyxwYXJ0bmVyLWJyb3dzZS1naWdhLXByb2plY3QtcmVxdWVzdCxwYXJ0bmVyLXZpZXctcHJvamVjdC1kZXRhaWxzLHZpZXctcGVybWl0LWRldGFpbHMtc3VwZXJ2aXNvcixicm93c2UtcGVybWl0LWxpc3Qtc3VwZXJ2aXNvcixjYW5jZWwtcXVhbGlmaWNhdGlvbi1jZXJ0aWZpY2F0ZSxjcmVhdGUtb2JqZWN0aW9uLHZpZXctY2xvc3VyZS1wZXJtaXQtcmVxdWVzdHMtc3VwZXJ2aXNvcixjYW5jZWwtZW5jcm9hY2htZW50LXJlcG9ydCxjb29yZGluYXRlLXdpdGhvdXQtbm90ZS1wYXJ0bmVyLHZpZXctY2xvc3VyZS1wZXJtaXQtcmVxdWVzdC1kZXRhaWxzLW9tYSxwYXJ0bmVyLXN1Ym1pdC1hZGQtcHJvamVjdC1jaGFuZ2UtcmVxdWVzdCxyZWd1bGFyaXR5LXBhcnRuZXItYnJvd3NlLXYyLXBlcm1pdC1yZXF1ZXN0cyxwYXJ0bmVyLWV4cG9ydC1wcm9qZWN0LXJlcXVlc3RzLXRvLWV4Y2VsLGJyb3dzZS1saW5rZWQtcHJvZmlsZS1lbmNyb2FjaG1lbnQtcmVwb3J0cyxyZWd1bGFyaXR5LXBhcnRuZXItdmlldy1ibG9ja2luZy1yZXF1ZXN0LWRldGFpbHMiLCJleHRyYS1kYXRhIjp7InVzZXItdHlwZSI6IlNVUEVSVklTT1JfVVNFUiIsInByb2ZpbGVzIjoiW3tcInByb2ZpbGVJZFwiOjEwMDMxLFwicHJvZmlsZVR5cGVcIjpcIkdPVkVSTk1FTlRcIixcImNvbnRyYWN0b3JUeXBlc1wiOm51bGwsXCJwYXJ0bmVyVHlwZXNcIjpbXCJTVVBFUlZJU09SXCIsXCJDT09SRElOQVRPUlwiLFwiQkxPQ0tFUlwiLFwiUEVSTUlUX0NMT1NVUkVfU1VQRVJWSVNPUlwiXSxcInN1YlByb2ZpbGVzSWRzXCI6W10sXCJkZWZhdWx0UHJvZmlsZVwiOnRydWUsXCJhZG1pblwiOmZhbHNlfV0iLCJmdWxsTmFtZSI6ItmF2KzYp9mH2K8g2YXYrdmF2K8g2LPZg9mK2YbZiiIsInVzZXJJZCI6IjgzMjA0In0sInRva2VuX3R5cGUiOiJBQ0NFU1NfVE9LRU4iLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0IiwiaWF0IjoxNzc4NDE3OTk5LCJleHAiOjE3Nzg0MTk3OTl9.PI-3ZDg-w8n5d7MV9KmxKKujFA63x0mi-86b9Ad5KtffcsVse-ihdXS1C-58J0J9nVap3K-odsCimg93vbNizg"

headers = {
    "X-Authorization": TOKEN,
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0",
    "Origin": "https://es.ripc.gov.sa",
    "Referer": "https://es.ripc.gov.sa/ripc-main/"
}

# =========================
#  Request IDs
# =========================
raw_ids = """
63053 
63430 
63752
63755
63874
63968
63985 
63993
64012
64011
63949
63909
63911
63910
63923
63921
63922
63058 
63056
63057 
63972
63971
64192 
64501 
64500 
64499 
64498 
63813 
63873
64573
64575
64566
64558
64724
64723
64114
64110
64107
64109
64108
64921 
64920 
64013
64387
64333
64336
63231
63362
63699
"""

request_ids = [i.strip() for i in raw_ids.splitlines() if i.strip().isdigit()]
print(f"عدد الطلبات: {len(request_ids)} -> {request_ids}")

# =========================
#  ArcGIS URLs
# =========================
PERMIT_URL = "https://es.ripc.gov.sa/arcgis/rest/services/RIPCLayers/PermitPath/FeatureServer/0/query"
RESTRICT_URL = "https://es.ripc.gov.sa/arcgis/rest/services/RIPCLayers/StreetBlocks/FeatureServer/0/query"

# =========================
#  API URLs
# =========================
API_BASE = "https://es.ripc.gov.sa/gateway/prmt-be"


def fetch_features(service_url, map_field, map_id):
    params = {
        "where": f"{map_field} = '{map_id}'",
        "outFields": "*",
        "f": "json",
        "outSR": 32638,
        "returnGeometry": "true"
    }

    try:
        r = requests.get(service_url, params=params, timeout=60)
        r.raise_for_status()
        js = r.json()
        return js.get("features", []) or []

    except requests.exceptions.Timeout:
        print(f"Timeout من ArcGIS | MapId={map_id}")

    except Exception as e:
        print(f"خطأ ArcGIS | MapId={map_id}: {e}")

    return []


def parse_date(val):
    if not val:
        return None
    try:
        return datetime.strptime(val, "%d-%m-%Y")
    except Exception:
        return None


def clip_text(val, max_len):
    if val is None:
        return None
    s = str(val)
    return s[:max_len - 1] if len(s) >= max_len else s


def uniq_clean(values):
    out = []
    seen = set()

    for v in values:
        if not v:
            continue

        v = str(v).strip()
        if not v:
            continue

        parts = [p.strip() for p in v.split(",") if p.strip()]

        for p in parts:
            if p not in seen:
                seen.add(p)
                out.append(p)

    return out


def get_unblocking_details(req_id):
    """
    يجرب V2 أولاً، ثم V1 إذا فشل.
    """

    # V2
    url_v2 = f"{API_BASE}/V2/api/unblocking/permit/{req_id}"

    try:
        r = requests.get(url_v2, headers=headers, timeout=60, allow_redirects=False)
        print(f"V2 Status {r.status_code} | RequestID={req_id}")

        if r.status_code == 200:
            js = r.json()
            data = js.get("data", {}) or {}
            if data:
                return data, "V2"

        elif r.status_code in [301, 302]:
            print("Redirect في V2 إلى:", r.headers.get("Location"))

        else:
            print("V2 Response:", r.text[:300])

    except Exception as e:
        print(f"خطأ V2 للطلب {req_id}: {e}")

    # V1
    url_v1 = f"{API_BASE}/api/v1/unblocking/{req_id}"

    try:
        r = requests.get(url_v1, headers=headers, timeout=60, allow_redirects=False)
        print(f"V1 Status {r.status_code} | RequestID={req_id}")

        if r.status_code == 200:
            js = r.json()
            data = js.get("data", {}) or {}
            if data:
                return data, "V1"

        elif r.status_code in [301, 302]:
            print("Redirect في V1 إلى:", r.headers.get("Location"))

        else:
            print("V1 Response:", r.text[:300])

    except Exception as e:
        print(f"خطأ V1 للطلب {req_id}: {e}")

    return {}, None


# =========================
#  Output
# =========================
output_dir = r"C:\Users\PC\Desktop\Scripts"
os.makedirs(output_dir, exist_ok=True)

gdb_path = os.path.join(output_dir, "UnblockingRoutes.gdb")
fc_name = "BasicRoutes"
fc_path = os.path.join(gdb_path, fc_name)

# =========================
#  Create GDB + Feature Class
# =========================
if not arcpy.Exists(gdb_path):
    arcpy.CreateFileGDB_management(output_dir, "UnblockingRoutes.gdb")

if arcpy.Exists(fc_path):
    try:
        arcpy.Delete_management(fc_path)
    except Exception:
        print("لم يتم حذف Feature Class. تأكد أنه غير مفتوح في ArcGIS Pro.")
        raise

spatial_ref = arcpy.SpatialReference(32638)
arcpy.CreateFeatureclass_management(
    gdb_path,
    fc_name,
    "POLYLINE",
    spatial_reference=spatial_ref
)

# =========================
#  Fields
# =========================
STREETNAME_LEN = 500
GOV_LEN = 1000
NEIGH_LEN = 1000

fields = [
    ("RequestID", "LONG"),
    ("BlockingId", "TEXT", 50),
    ("PermitRequestDate", "DATE"),
    ("PermitReqNum", "TEXT", 50),
    ("ContractorName", "TEXT", 255),
    ("OwnerEntity", "TEXT", 255),
    ("SubServiceType", "TEXT", 100),
    ("StreetName", "TEXT", STREETNAME_LEN),

    ("PathLength", "DOUBLE"),
    ("PathWidth", "DOUBLE"),
    ("PathDepth", "DOUBLE"),
    ("StreetWidth", "DOUBLE"),
    ("PermitType", "TEXT", 50),
    ("RestrictionReason", "TEXT", 255),

    ("GovName", "TEXT", GOV_LEN),
    ("Neighborhood", "TEXT", NEIGH_LEN),

    ("XCoord", "DOUBLE"),
    ("YCoord", "DOUBLE"),

    ("MapType", "TEXT", 20),
    ("MapId", "TEXT", 100),
    ("Source", "TEXT", 10)
]

for f in fields:
    if len(f) == 2:
        arcpy.AddField_management(fc_path, f[0], f[1])
    else:
        arcpy.AddField_management(fc_path, f[0], f[1], field_length=f[2])

# =========================
#  Insert Data
# =========================
excel_rows = []

cursor_fields = [
    "SHAPE@",
    "RequestID",
    "BlockingId",
    "PermitRequestDate",
    "PermitReqNum",
    "ContractorName",
    "OwnerEntity",
    "SubServiceType",
    "StreetName",
    "PathLength",
    "PathWidth",
    "PathDepth",
    "StreetWidth",
    "PermitType",
    "RestrictionReason",
    "GovName",
    "Neighborhood",
    "XCoord",
    "YCoord",
    "MapType",
    "MapId",
    "Source"
]

with arcpy.da.InsertCursor(fc_path, cursor_fields) as cursor:

    for req_id in request_ids:
        print("\n==============================")
        print(f"معالجة الطلب: {req_id}")

        data, source = get_unblocking_details(req_id)

        if not data:
            print(f"لا توجد بيانات للطلب {req_id}")
            continue

        permit = data.get("permitDetailModel", {}) or {}
        block = data.get("blockingRequestDetailModel", {}) or {}

        permit_map_id = permit.get("permitMapId")
        restr_map_id = block.get("gisMapId")

        contractor_name = (permit.get("contractor") or {}).get("name", "") or ""
        owner_entity = (permit.get("project") or {}).get("projectSupervisorEntityAr", "") or ""

        sub_service = (
            (permit.get("excavationDetails") or {})
            .get("subserviceTypes", {})
            .get("descAr", "")
            or ""
        )

        street_name = block.get("streetName", "") or ""
        street_name_gdb = clip_text(street_name, STREETNAME_LEN)

        permit_req_num = permit.get("requestId", "") or ""
        permit_date_str = permit.get("permitRequestDate")
        permit_date = parse_date(permit_date_str)

        blocking_id = str(data.get("blockingId", ""))

        permit_type = ""
        if permit.get("permitType"):
            permit_type = (permit["permitType"] or {}).get("descAr", "") or ""

        restriction_reason = block.get("restrictionReason", "") or ""

        gov_name = ""
        neighborhood = ""

        routes_block = block.get("routeInformationDetailModel") or []
        if routes_block and isinstance(routes_block, list):
            govs = uniq_clean([
                r.get("governorate")
                for r in routes_block
                if isinstance(r, dict)
            ])
            dists = uniq_clean([
                r.get("district")
                for r in routes_block
                if isinstance(r, dict)
            ])

            gov_name = ",".join(govs)
            neighborhood = ",".join(dists)

        contractor_name = clip_text(contractor_name, 255)
        owner_entity = clip_text(owner_entity, 255)
        sub_service = clip_text(sub_service, 100)
        permit_req_num = clip_text(permit_req_num, 50)
        permit_type = clip_text(permit_type, 50)
        restriction_reason = clip_text(restriction_reason, 255)
        gov_name = clip_text(gov_name, GOV_LEN)
        neighborhood = clip_text(neighborhood, NEIGH_LEN)

        path_length = None
        path_width = None
        path_depth = None
        street_width = None
        x_coord = None
        y_coord = None

        routes_permit = permit.get("tblPermitRoutesDtos") or []

        if routes_permit and isinstance(routes_permit, list):
            r0 = routes_permit[0] or {}

            path_length = r0.get("pathLength")
            path_width = r0.get("pathWidth")
            path_depth = r0.get("pathDepth")
            x_coord = r0.get("xCoordinate")
            y_coord = r0.get("yCoordinate")

            street_info_raw = r0.get("streetInfo")

            try:
                if street_info_raw:
                    info_list = json.loads(street_info_raw)
                    if isinstance(info_list, list) and info_list:
                        street_width = (info_list[0] or {}).get("streetWidth")
            except Exception:
                street_width = None

        work_path = permit.get("workPath") or {}

        if path_length is None:
            path_length = work_path.get("pathLength")
        if path_width is None:
            path_width = work_path.get("pathWidth")
        if path_depth is None:
            path_depth = work_path.get("pathDepth")
        if street_width is None:
            street_width = work_path.get("streetWidth")

        inserted_any = False

        # =========================
        #  Permit Geometry
        # =========================
        if permit_map_id:
            fs = fetch_features(PERMIT_URL, "PermitMapId", permit_map_id)
            print(f"PermitMapId={permit_map_id} | Features={len(fs)}")

            for feat in fs:
                geom = (feat or {}).get("geometry") or {}

                if geom and "paths" in geom:
                    try:
                        polyline = arcpy.AsShape(
                            {
                                "paths": geom["paths"],
                                "spatialReference": {"wkid": 32638}
                            },
                            True
                        )

                        cursor.insertRow([
                            polyline,
                            int(req_id),
                            blocking_id,
                            permit_date,
                            permit_req_num,
                            contractor_name,
                            owner_entity,
                            sub_service,
                            street_name_gdb,
                            path_length,
                            path_width,
                            path_depth,
                            street_width,
                            permit_type,
                            restriction_reason,
                            gov_name,
                            neighborhood,
                            x_coord,
                            y_coord,
                            "Permit",
                            str(permit_map_id),
                            source
                        ])

                        inserted_any = True

                    except Exception as e:
                        print(f"خطأ إدخال Permit للطلب {req_id}: {e}")

        # =========================
        #  Restriction Geometry
        # =========================
        if restr_map_id:
            fs = fetch_features(RESTRICT_URL, "BlockingMapID", restr_map_id)
            print(f"BlockingMapID={restr_map_id} | Features={len(fs)}")

            for feat in fs:
                geom = (feat or {}).get("geometry") or {}

                if geom and "paths" in geom:
                    try:
                        polyline = arcpy.AsShape(
                            {
                                "paths": geom["paths"],
                                "spatialReference": {"wkid": 32638}
                            },
                            True
                        )

                        cursor.insertRow([
                            polyline,
                            int(req_id),
                            blocking_id,
                            permit_date,
                            permit_req_num,
                            contractor_name,
                            owner_entity,
                            sub_service,
                            street_name_gdb,
                            path_length,
                            path_width,
                            path_depth,
                            street_width,
                            permit_type,
                            restriction_reason,
                            gov_name,
                            neighborhood,
                            x_coord,
                            y_coord,
                            "Restriction",
                            str(restr_map_id),
                            source
                        ])

                        inserted_any = True

                    except Exception as e:
                        print(f"خطأ إدخال Restriction للطلب {req_id}: {e}")

        if not inserted_any:
            print(f"تنبيه: الطلب {req_id} لا يحتوي Geometry من Permit أو Restriction")

        # =========================
        #  Excel Row
        # =========================
        excel_rows.append({
            "RequestID": req_id,
            "BlockingId": blocking_id,
            "PermitRequestDate": permit_date_str or "",
            "PermitReqNum": permit_req_num,
            "ContractorName": contractor_name,
            "OwnerEntity": owner_entity,
            "SubServiceType": sub_service,
            "StreetName": street_name,
            "PathLength": path_length,
            "PathWidth": path_width,
            "PathDepth": path_depth,
            "StreetWidth": street_width,
            "PermitType": permit_type,
            "RestrictionReason": restriction_reason,
            "GovName": gov_name,
            "Neighborhood": neighborhood,
            "XCoord": x_coord,
            "YCoord": y_coord,
            "PermitMapId": permit_map_id,
            "BlockingMapId": restr_map_id,
            "Source": source
        })

# =========================
#  Export Excel
# =========================
df = pd.DataFrame(excel_rows)

excel_path = os.path.join(output_dir, "Unblocking_Basic.xlsx")
df.to_excel(excel_path, index=False, engine="openpyxl")

# =========================
#  Count Features
# =========================
try:
    cnt = int(arcpy.management.GetCount(fc_path)[0])
    print(f"\nعدد Features داخل Feature Class: {cnt}")
except Exception as e:
    print(f"\nلم يتم حساب عدد Features: {e}")

print(f"\nتم الحفظ في GDB:")
print(fc_path)

print(f"\nتم الحفظ في Excel:")
print(excel_path)

