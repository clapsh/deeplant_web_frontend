from flask import send_file
import firebase_admin  # Firestore init
from datetime import datetime # 시간 출력용
from firebase_admin import firestore, storage
import keyId
import io
import os

KEY_PATH = "serviceAccountKey.json"


# FireBase Data(FireStore & FireStorage)
class FireBase_:
    def __init__(self):
        # 1. Making FireStore Connection
        cred = firebase_admin.credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)
        self.firebase_db = firestore.client()
        self.fix_data_state = dict()  # 바뀐게 있는 데이터 저장

        # 2. Making FireStorage Connection
        self.bucket = storage.bucket(keyId.firebase_bucket_address)
        # 2-1. 저장할 이미지 디렉토리가 없다면 생성합니다.
        os.makedirs('images/meats', exist_ok=True)
        os.makedirs('images/qr_codes',exist_ok = True)

        # 3. Making Buffer Data (Firebase -> Flask Server )
        self.temp_data = dict()  # 버퍼
        self.temp_normal_data = dict() # 일반
        self.temp_researcher_data = dict() # 직원
        self.temp_manager_data = dict() # 관리자
        self.temp_meat_data = dict()

    def print_flask_database(self):
        print(f"transfer normal data: {self.temp_normal_data}")
        print(f"transfer researcher data: {self.temp_researcher_data}")
        print(f"transfer manager data: {self.temp_manager_data}")
        print(f"transfer meat data: {self.temp_meat_data}")

    def transferDbData(self):
        print("1. Trasfer DB&Image Data [Firebase -> Flask Server]",datetime.now())
        # 1. 바뀐 데이터 확인
        self.firestoreCheck()

        # 2. 데이터 가져오기 (firestore -> Flask Server)
        if self.fix_data_state["fix_data"]["users_1"]:
            # 1. firestore -> server 가져오기
            self.firestore2server("users_1")
            # 2. 버퍼에 있는 데이터 채워두기
            self.temp_normal_data = self.temp_data
        if self.fix_data_state["fix_data"]["users_2"]:
            # 1. firestore -> server 가져오기
            self.firestore2server("users_2")
            # 2. 버퍼에 있는 데이터 채워두기
            self.temp_researcher_data = self.temp_data
        if self.fix_data_state["fix_data"]["users_3"]:
            # 1. firestore -> server 가져오기
            self.firestore2server("users_3")
            # 2. 버퍼에 있는 데이터 채워두기
            self.temp_manager_data = self.temp_data
        if self.fix_data_state["fix_data"]["meat"]:
            # 1. firestore -> server 가져오기
            self.firestore2server("meat")
            # 2. 버퍼에 있는 데이터 채워두기
            self.temp_meat_data = self.temp_data
            # 3. fire storage -> server
            self.firestorage2server()

        # 3. 데이터 AWS RDS, S3에 저장하기(Flask Server -> S3 or RDS)
        self.print_flask_database()

    def firestoreCheck(self):  # Firestore Data 바뀐게 있는지 확인하는 method
        # 1. 0-0-0-0-0 document에서 바뀐 데이터 수합
        doc_ref = self.firebase_db.collection("meat").document("0-0-0-0-0")
        self.fix_data_state = doc_ref.get().to_dict()

        # 2. 바뀐 데이터 수합했으면 비워야 한다.
        doc_ref.update({"fix_data":{"users_1": [], "users_2": [], "users_3": [], "meat": []}})

    def firestore2server(
        self, collection
    ):  # Firestore에서 data 가져오기 (Firestore -> Flask Server)
        self.temp_data = dict()
        doc_ref = self.firebase_db.collection(collection)
        items = self.fix_data_state["fix_data"][
            collection
        ]  # users database -> uid 목록, meat database -> 관리번호 목록
        # 1. 바뀌었다고 한 id 대로 데이터 가져오기
        for i in items:
            doc = doc_ref.document(i).get().to_dict()
            self.temp_data[i] = doc

    def firestorage2server(self):
        # 'meat' 컬렉션의 문서 ID가 있는 리스트를 가져옵니다.
        items = self.fix_data_state["fix_data"]["meat"]

        for item_id in items:
            # Firebase Storage에서 해당 파일을 찾아 blob으로 가져옵니다.
            blob_meats = self.bucket.blob(f"meats/{item_id}.png")
            blob_qr_codes = self.bucket.blob(f"qr_codes/{item_id}.png")

            # blob이 존재하는지 확인하고 존재하면 파일로 저장합니다.
            if blob_meats.exists():
                blob_meats.download_to_filename(f"./images/meats/{item_id}.png")
            else:
                print(f"No such file: meats/{item_id}.png")

            if blob_qr_codes.exists():
                blob_qr_codes.download_to_filename(f"./images/qr_codes/{item_id}.png")
            else:
                print(f"No such file: qr_codes/{item_id}.png")
                
    def server2firestore(self,collection,document_id,data):  # Firestore에 data 넣기 (Firestore <- Flask Server)
        doc_ref = self.firebase_db.collection(collection).document(document_id)
        doc_ref.set(data,merge=True)

    def server2firestorage(self,filepath,blob_name): # Firebase Storage에 image 데이터 넣기 (Storage <- Flask Server)
        blob = self.bucket.blob(blob_name)
        blob.upload_from_filename(filename=filepath,content_type="image/png")