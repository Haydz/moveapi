import json
json_test = {'TableNames': ['AttendanceSessionSettings-', 'AttendanceSessionSettings-TC-1589-manage-dependencies', 'AttendanceSessionSettings-TC-2235', 'AttendanceSessionSettings-TC-2235-redo', 'AttendanceSessionSettings-TC-2236', 'AttendanceSessionSettings-howardlu-dev', 'AttendanceSessionSettings-master', 'AttendanceSessionSettings-mihadrv', 'AttendanceSessionSettings-remove-dd-logs-from-dev', 'AttendanceSessionSettings-rockyken-dev', 'AttendanceSessionSettings-roddy-dev', 'AttendanceSessionSettings-rodrigo-test', 'AttendanceSessionSettings-rodrigomedeiros-dev', 'AttendanceSessionSettings-shilpabhat-dev', 'AttendanceSessionSettings-tc-1146', 'AttendanceSessionSettings-tc-1146-jenkins-deploy-test', 'AttendanceSessionSettings-tc-2150-fix-outlier-info', 'AttendanceSessionSettings-tc-2150-implement-outlier-algorithm', 'AttendanceSessionSettings-tc-788-errors-cleanup', 'AttendanceSessionSettings-tc-788-fix-400-error', 'AttendanceSessionSettings-test', 'AttendanceSessionSettings-try-fresh', 'EmrFSMetadata', 'ExamBehaviourLocksV2-lemaianh-dev', 'ExamBehaviourLocksV2-master', 'ExamBehaviourLocksV2-nhungngo-dev', 'ExamBehavioursV2-lemaianh-dev', 'ExamBehavioursV2-master', 'ExamBehavioursV2-nhungngo-dev', 'ExamEventsV2-lemaianh-dev', 'ExamEventsV2-master', 'ExamEventsV2-nhungngo-dev', 'ExamSettingsV2-lemaianh-dev', 'ExamSettingsV2-master', 'ExamSettingsV2-nhungngo-dev', 'MOCK_ATTENDANCE_TABLE_NAME', 'Movies', 'Permissions-authorization-service-marc-dev', 'Permissions-authorization-service-michaelweeks-dev-infrastructure', 'Permissions-authorization-service-mw-dev-infrastructure', 'Permissions-authorization-service-sandbox-infrastructure', 'SecretListingEvents', 'SentUuid-caliper-service-halsey-dev-infrastructure', 'SentUuid-caliper-service-sandbox-infrastructure', 'TestStreaming', 'Thread', 'UserAttendance-', 'UserAttendance-TC-1589-manage-dependencies', 'UserAttendance-TC-2235', 'UserAttendance-TC-2235-redo', 'UserAttendance-TC-2236', 'UserAttendance-howardlu-dev', 'UserAttendance-master', 'UserAttendance-mihadrv', 'UserAttendance-remove-dd-logs-from-dev', 'UserAttendance-rockyken-dev', 'UserAttendance-roddy-dev', 'UserAttendance-rodrigo-test', 'UserAttendance-rodrigomedeiros-dev', 'UserAttendance-sas-60', 'UserAttendance-shilpabhat-dev', 'UserAttendance-tc-1146', 'UserAttendance-tc-1146-jenkins-deploy-test', 'UserAttendance-tc-2150-fix-outlier-info', 'UserAttendance-tc-2150-implement-outlier-algorithm', 'UserAttendance-tc-788-errors-cleanup', 'UserAttendance-tc-788-fix-400-error', 'UserAttendance-test', 'UserAttendance-try-fresh', 'asset-manifest-service-sandbox-versions', 'boilerplate-service-matthaber2-dev-importTest', 'data-eng-dev-lakeformation-state-lock', 'data-eng-terraform-dev-state-locks', 'fe-apps-minimum-version', 'fe-micro-apps-versions', 'kongstaging', 'platform-maintenance-schedule', 'serverless-authentication-cache-dev', 'serverless-authentication-users-dev', 'sessions', 'snowplow-enrich-server', 'snowplow-enrich-server-config', 'snowplow-s3-loader-bad-server', 'snowplow-s3-loader-enriched-server', 'snowplow-s3-loader-raw-server', 'sns-history', 'sns-mapper', 'sns-preferences', 'terraform-dev-state-locks', 'th-developer-docs-metadata', 'th-developer-docs-metadata-staging', 'yash-temp'], 'ResponseMetadata': {'RequestId': 'LGPASO5MQ11CFTO43V73C7NVGVVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Tue, 17 Sep 2024 13:35:15 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '3150', 'connection': 'keep-alive', 'x-amzn-requestid': 'LGPASO5MQ11CFTO43V73C7NVGVVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2353246533'}, 'RetryAttempts': 0}}

converted = json.dumps(json_test)


dict_json = json.loads(converted)
print(dict_json)

for table in dict_json["TableNames"]:
    if table == "sessions":
        print(f"table found: sessions")


movie_response = {'Item': {'year': {'N': '1996'}, 'title': {'S': 'Fear'}}, 'ResponseMetadata': {'RequestId': 'CFS2DTI4FOCQ9DLDLAQ0MQLIU7VV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Tue, 17 Sep 2024 19:52:41 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '51', 'connection': 'keep-alive', 'x-amzn-requestid': 'CFS2DTI4FOCQ9DLDLAQ0MQLIU7VV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '582330499'}, 'RetryAttempts': 0}}

year = movie_response['Item']['year']['N']
print(year)

for key, value in movie_response["Item"].items():
    print(value)
    for key , v in value.items():
        print(v)
   
   