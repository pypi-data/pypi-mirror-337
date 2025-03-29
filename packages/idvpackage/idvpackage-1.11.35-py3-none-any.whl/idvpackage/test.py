import json
import base64
import json
import time
import re
import pandas as pd
import os

start = time.time()
from idvpackage import ocr
end = time.time()
print(f'Time taken to import: {end - start}')

# creds= {
#   "type": "service_account",
#   "project_id": "spotii-me",
#   "private_key_id": "8297a634a3dc73c8551e8be9e000a022e7a9ff62",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCb0wV5KggdcIO3\n6P0iYFQ1GEcbebFP6oKYkjTfy7NipxK1NB/B0pbm5jAtPZ9Hi36aOrxsdtgPW1Y3\nbk3NqCUu+LqFlfm8qDBGQD8MzalSHhh2FHtxAu0FoVwwrfAFncWNBBvzfwTbfvn9\nrn45UKeclGwGiLcjJ52YPItX7PwfCMsvdfaXwU1lLbiItHcdRbw7M3ZErpvNs+dJ\nNGs9bNHit5ygwXZxFV5BlhgRKF3HSECe/pZ3IRaVMMSWFqgeOsDa5fFcaJj37xcN\nDNRf7X6deGrNVHT7Dcu6YLGAqft6kOjUNxcU9tHwRN5LqVyon2rmQDvp63sWkdLx\n9A0zeBkFAgMBAAECggEAA/LdQuSEh6B0CgtKrN4VjDHlDWZwTpbh/9VGpzwte8zB\njdt4CYyZW9kN8/uJh4Har7RY1YPOdlcpcGaobJN7+7x8V4nFJhl5/bG/l0a36XeP\nRaC/vw2krX2ZDTe/KxlEKg5mWe2IVTqawam0E6Y+VRqywRiiUW790J+KJWyBOBUS\nES3ydPQngTLmAmLDIbN+1hOwl7WUvNCO04Y2lgb3TLODVLRXl3J0Es0CGBFeeRV3\nrLFlWCZE95AF9DvYvPkeMPNnTnqUF9kVW6o9O0yKziWhi3nkEeX9u1RF68tbkkVL\nqC4yaDB4elkRbaNNecJifhyXGRhN4ijaxywkfeOWqQKBgQDWX3iB4jQXm4vlbmR8\nyETi2aVAGrP/QJl8gJsr25NVhPUlgNlTS5COks+lkuIbVrwnPl94YA+ACZzstkry\n34ycgDwwLRUK2SPbDOBGgGkblQ6PS4Z8GD/D4ysCKG/SWGH6ofqbVzMFPHlvLij6\n6YwrEAdmB+mxO8MAVC6Kh22LnQKBgQC6FRWY8vZOb26xVtm0qcPDNhT8uJ2Np00c\nHgdUilf9hA45RzAKNQrM8inZkUde7PQIFpTcaplV1ExHIP4Auko6seVU1mayZQ7L\n0f3wyoyn/A2SHc+84MqejBnIxL4N6CD9xNBzgw252OYFOQ7pdqXEGH4XovnQkNGv\nHqad/WFKiQKBgQC3pRvoMK8tliwXRSXCnBIfQBJHw1h1j5KtTMMhpD4oYflcwm/q\n4m4ZJX3LOvSGNRyEhfNlfO1qY1HSmyvDumyL2XM2VjiTjYcg7XvoCbOBVIUfjrTL\n9D4UArTiaV+6E8sD2eWFVAM6Nh9VdnbW1GImtdmQt7CkCy03R+aC+BeJJQKBgGrf\ngS//GwehaGnh/9eLSSvs+9DKF3MsC1WCyaL8cdzg42pyQF0cab+btf2HOv6CCQY8\nMfMGJlrtO4H+qOOyGr/rPFOlcAY1lHHrgXWyX2Z7lS++f3lzgevde1Gb7av/DjOx\nvicZteBvemy1gKMFyd7+Ui0xJVlsU4HIkNlclWxBAoGACjR0dtTRPEOSthyFkurk\nnLFXWTHK4oPXBMmngqb8DsrQwKhbpEzS2MzCgf2Bg2lY4JI7SyD/OIVDpcW6+sVZ\nAfsTN3TPLQfIJ2LoDV2PGx7HpVRZDk4tBlco6AuABrkFwBHDjCMRlL/UaqrwDYPV\nG7T5FipEBm6OhdAbyncSIt8=\n-----END PRIVATE KEY-----\n",
#   "client_email": "spotii-gapi-10-2023@spotii-me.iam.gserviceaccount.com",
#   "client_id": "111897133454311774587",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/spotii-gapi-10-2023%40spotii-me.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"
# }
#
#
# credentials_string = json.dumps(creds)
# api_key = "AIzaSyA3nIy5Hx_80EnF_kJWZPOEkLLFuQw_yms"
# # genai_key = "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"
# genai_key = "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"
#
# # idv = ocr.IdentityVerification(credentials_string, api_key=api_key, genai_key=genai_key)
# start = time.time()
# idv = ocr.IdentityVerification(credentials_string=credentials_string, api_key=api_key)
# end = time.time()
# print(f'Time taken to initialize: {end - start}')
#
# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         image_data = image_file.read()
#         base64_encoded = base64.b64encode(image_data).decode("utf-8")
#
#         return base64_encoded
#
#
# data_df = pd.read_csv("users_28th_Feb.csv")
# base = '/Users/husunshujaat/Downloads/users_28_Feb'
# id_list = data_df['national_id_front'].tolist()
#
# ids_done = [file for file in os.listdir('/Users/husunshujaat/Downloads/users_28_Feb') if file.endswith('.csv')]
#
# for i in range(len(ids_done)):
#     ids_done[i] = ids_done[i][:36]
#     ids_done[i] = ids_done[i]
#
#
# rem_ids = []
# for id in id_list:
#     if id not in ids_done:
#         final = id+'.jpg'
#         rem_ids.append(final)
#
# print(len(id_list))
# print(len(ids_done))
# print(len(rem_ids))
#
#
# for i in range(len(id_list)):
#     id_list[i] = id_list[i] + '.jpg'
#
# def process_user_ids(file):
#     #gc.collect()
#     front_base64 = image_to_base64(os.path.join(base, file))
#     front = idv.extract_front_id_info(front_base64, country='QAT', nationality='QAT')
#     csv_file = file.strip('.jpg') + ".csv"
#     df = pd.DataFrame([front])
#     df['user_id'] = file[:36]
#     df.to_csv(os.path.join(base, csv_file), index=False)
#     print(f'Finished user_id: {file[:36]}')

#process_user_ids(id_list[-1])

# ==========Using ThreadPoolExecutor================

# import concurrent.futures
#
#
#
# # Main function to run threads
# def main():
#     num_threads = 4
#     try:
#         with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
#             executor.map(process_user_ids, rem_ids)
#             #executor.shutdown()
#
#     except Exception as e:
#         print(f"The Exception was {e}")
#
#
# import time
# from datetime import datetime
# import gc
# if __name__ == "__main__":
#     gc.collect()
#     current_datetime = datetime.now()
#     start = time.time()
#     main()
#     print(f"Script took {(time.time() - start) / 60} minutes to run. ")
#     # for id in rem_ids:
#     #      process_user_ids(id)
#     #      print(f"Script took {(time.time() - start) / 60} minutes to run. ")
#
#      # Forces garbage collection

# # cb740341-7193-47d4-a155-7fab3da7b983.jpg
# # 11efd60e-dbaf-4954-9f9d-5e6fe05db12a_1730389749_a6cc63.png
#
# base = "/Users/husunshujaat/Downloads/Lebanese Documents Latest"
#
# report = []
#
# files = [file for file in os.listdir(base) if (file.endswith('jpg') or file.endswith('.JPG') or file.endswith('.png'))]
#
#
# print(len(files))
#
# for file in files:
#   country = 'LBN'
#   nationality = 'LBN'
#
#   front_image_path = os.path.join(base,file)
#   print(front_image_path)
#   front_img_base64 = image_to_base64(front_image_path)
#
#   original_start = time.time()
#   passport_data = idv.exract_passport_info(front_img_base64, country, nationality)
#   overall_time = round((time.time() - original_start), 2)
#   print(f'Total time: %.2f seconds' % overall_time)
#   print(f"\n\n Passport Data: {passport_data}")
#   # print(passport_data['id_number'])
#   # print(passport_data['error'])
#   report.append(passport_data)
#
# df = pd.DataFrame(report)
# print(len(df))
# df.to_csv(os.path.join(base, "lebanese_passport_check.csv"),index=False)
#==========================================SIMILARITY REPORT================================================
creds = {
    "type": "service_account",
    "project_id": "spotii-me",
    "private_key_id": "8297a634a3dc73c8551e8be9e000a022e7a9ff62",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCb0wV5KggdcIO3\n6P0iYFQ1GEcbebFP6oKYkjTfy7NipxK1NB/B0pbm5jAtPZ9Hi36aOrxsdtgPW1Y3\nbk3NqCUu+LqFlfm8qDBGQD8MzalSHhh2FHtxAu0FoVwwrfAFncWNBBvzfwTbfvn9\nrn45UKeclGwGiLcjJ52YPItX7PwfCMsvdfaXwU1lLbiItHcdRbw7M3ZErpvNs+dJ\nNGs9bNHit5ygwXZxFV5BlhgRKF3HSECe/pZ3IRaVMMSWFqgeOsDa5fFcaJj37xcN\nDNRf7X6deGrNVHT7Dcu6YLGAqft6kOjUNxcU9tHwRN5LqVyon2rmQDvp63sWkdLx\n9A0zeBkFAgMBAAECggEAA/LdQuSEh6B0CgtKrN4VjDHlDWZwTpbh/9VGpzwte8zB\njdt4CYyZW9kN8/uJh4Har7RY1YPOdlcpcGaobJN7+7x8V4nFJhl5/bG/l0a36XeP\nRaC/vw2krX2ZDTe/KxlEKg5mWe2IVTqawam0E6Y+VRqywRiiUW790J+KJWyBOBUS\nES3ydPQngTLmAmLDIbN+1hOwl7WUvNCO04Y2lgb3TLODVLRXl3J0Es0CGBFeeRV3\nrLFlWCZE95AF9DvYvPkeMPNnTnqUF9kVW6o9O0yKziWhi3nkEeX9u1RF68tbkkVL\nqC4yaDB4elkRbaNNecJifhyXGRhN4ijaxywkfeOWqQKBgQDWX3iB4jQXm4vlbmR8\nyETi2aVAGrP/QJl8gJsr25NVhPUlgNlTS5COks+lkuIbVrwnPl94YA+ACZzstkry\n34ycgDwwLRUK2SPbDOBGgGkblQ6PS4Z8GD/D4ysCKG/SWGH6ofqbVzMFPHlvLij6\n6YwrEAdmB+mxO8MAVC6Kh22LnQKBgQC6FRWY8vZOb26xVtm0qcPDNhT8uJ2Np00c\nHgdUilf9hA45RzAKNQrM8inZkUde7PQIFpTcaplV1ExHIP4Auko6seVU1mayZQ7L\n0f3wyoyn/A2SHc+84MqejBnIxL4N6CD9xNBzgw252OYFOQ7pdqXEGH4XovnQkNGv\nHqad/WFKiQKBgQC3pRvoMK8tliwXRSXCnBIfQBJHw1h1j5KtTMMhpD4oYflcwm/q\n4m4ZJX3LOvSGNRyEhfNlfO1qY1HSmyvDumyL2XM2VjiTjYcg7XvoCbOBVIUfjrTL\n9D4UArTiaV+6E8sD2eWFVAM6Nh9VdnbW1GImtdmQt7CkCy03R+aC+BeJJQKBgGrf\ngS//GwehaGnh/9eLSSvs+9DKF3MsC1WCyaL8cdzg42pyQF0cab+btf2HOv6CCQY8\nMfMGJlrtO4H+qOOyGr/rPFOlcAY1lHHrgXWyX2Z7lS++f3lzgevde1Gb7av/DjOx\nvicZteBvemy1gKMFyd7+Ui0xJVlsU4HIkNlclWxBAoGACjR0dtTRPEOSthyFkurk\nnLFXWTHK4oPXBMmngqb8DsrQwKhbpEzS2MzCgf2Bg2lY4JI7SyD/OIVDpcW6+sVZ\nAfsTN3TPLQfIJ2LoDV2PGx7HpVRZDk4tBlco6AuABrkFwBHDjCMRlL/UaqrwDYPV\nG7T5FipEBm6OhdAbyncSIt8=\n-----END PRIVATE KEY-----\n",
    "client_email": "spotii-gapi-10-2023@spotii-me.iam.gserviceaccount.com",
    "client_id": "111897133454311774587",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/spotii-gapi-10-2023%40spotii-me.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

credentials_string = json.dumps(creds)
api_key = "AIzaSyA3nIy5Hx_80EnF_kJWZPOEkLLFuQw_yms"
#genai_key = "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"
genai_key = "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"

idv = ocr.IdentityVerification(credentials_string=credentials_string, api_key=genai_key)

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded = base64.b64encode(image_data).decode("utf-8")

        return base64_encoded

#front_id = image_to_base64("/Users/husunshujaat/Downloads/iraqi_dump/national_id-1/image-20250318-060853.png")
#back_id = image_to_base64("/Users/husunshujaat/Downloads/26fb162f-9c01-427a-a0bc-5a28cd209e7f_1742225057_c38200.png")
#passport = image_to_base64("/Users/husunshujaat/Downloads/Lebanese Documents Latest/ID Front 9.JPG")
#video = "/Users/husunshujaat/Downloads/15716ad9-d69a-4c0b-b637-d9988de2fd17_1742138543_819e84.mp4"
country = "LBN"
nationality="LBN"
import json

# Open and read the JSON file
step_data_path = "/Users/husunshujaat/Downloads/67a47d03ef69427f0deee213_step_data.json"

#problems = ['16.jpg', '26.jpg', '69.jpg', '2.jpg']
#problems = ['26.jpg']
output=[]
import time
start = time.time()
count = 0
for file in os.listdir("/Users/husunshujaat/Downloads/Lebanese Passports/"):
#for file in problems:
    if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.PNG') or file.endswith('.JPG'):
        print(file)
        front_image = image_to_base64(os.path.join("/Users/husunshujaat/Downloads/Lebanese Passports", file))
        x = idv.exract_passport_info(front_image, country)
        print(x)
        ans_dict ={}
        #try:
            # ans_dict['file'] = file
            # ans_dict['first_name'] = x['first_name']
            # ans_dict['last_name'] = x['last_name']
            # ans_dict['name'] = x['name']
            # ans_dict['gender'] = x['gender']
            # ans_dict['gender_ar'] = x['gender_ar']
            # ans_dict['father_name'] = x['father_name']
            # ans_dict['first_name_en'] = x['first_name_en']
            # ans_dict['father_name_en'] = x['father_name_en']
            # ans_dict['last_name_en'] = x['last_name_en']
            # ans_dict['name_en'] = x['name_en']
            # ans_dict['mother_last_name'] = x['mother_last_name']
            # ans_dict['mother_first_name'] = x['mother_first_name']
            # ans_dict['mother_last_name_en'] = x['mother_last_name_en']
            # ans_dict['mother_first_name_en'] = x['mother_first_name_en']
            # output.append(ans_dict)
        # except:
        #     x=2+1

        #print("==========================")
# pd.DataFrame(output).to_csv("/Users/husunshujaat/Downloads/surname_fix_result_mix_2.csv")
# try:
#     print(f"Script took {(time.time() - start)/60} minutes to run.")
# except Exception as e:
#     print(e)
#print(problems)


# ## Get reports
# with open(video, "rb") as video_file:
#     video_bytes = video_file.read()
# video_quality_result = idv.check_document_quality(video_bytes)
#
# selfie = {
#     'selfie': video_quality_result.get('selfie')
#     }
#passport_res = idv.extract_document_info(passport, 'front', 'national_id', country)
#print(f"\n\nPasspport result: {passport_res}")

#passport_res.update(selfie)

#doc_report, face_report = idv.extract_ocr_info(passport_res, video_bytes, country = 'SDN', report_names=['document', 'facial_similarity_video'])
# print(f"\n\nDOC Result: {doc_report}")
# print(f"\n\nFACIAL Result: {face_report}")

#========Experimentation========
# import os
# import pandas as pd
# jpg_files = [image_to_base64(files) for files in os.listdir("/Users/husunshujaat/project_idv_package/idvpackage/") if files.endswith(".jpg")]
# step_data_paths = [files for files in os.listdir("/Users/husunshujaat/project_idv_package/idvpackage/") if files.endswith(".json")]
# print(len(jpg_files))
# print(len(step_data_paths))
# report = []
# i=0
# for image in jpg_files:
#     for step_data in step_data_paths:
#         i+=1
#         print(i)
#         idv = ocr.IdentityVerification(genai_key=genai_key, credentials_string=credentials_string, api_key=api_key)
#         passport = idv.exract_passport_info(passport=image, country='IRQ', nationality='IRQ', step_data_path=step_data)
#         report.append(passport)
#
#
# df = pd.DataFrame(report)
# df.to_csv("passport_similarity_check_report.csv", index=False)
#

