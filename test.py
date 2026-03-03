import os
import re
import requests
import xml.etree.ElementTree as ET
#설정값
xml_file = "ProfileCatalog.xml"  # XML 파일경로
download_dir = "modules"  # 다운로드폴더
base_url = "http://deploy.ksd.or.kr/Deploy/modules_gzip/"  # 다운로드 URL기본경로
# 저장할디렉토리생성(없으면생성)
os.makedirs(download_dir, exist_ok=True)
# XML 파일 파싱및 DLL 파일명 추출
tree = ET.parse(xml_file)
root = tree.getroot()
dll_pattern = re.compile(r"([^\\]+\.dll)$")  # DLL 파일명 추출 정규식
dll_files = []
for module in root.findall("ModuleT"):
    module_filename = module.get("ModuleFileName", "")
    match = dll_pattern.search(module_filename)
    if match:
        dll_files.append(match.group(1))
# 추출된 DLL 파일 다운로드
for dll_name in dll_files:
    gz_filename = f"{dll_name}.gz"
    download_url = f"{base_url}{gz_filename}"
    save_path = os.path.join(download_dir, gz_filename)
    try:
        # 파일 다운로드 요청
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
        # 파일 저장
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024
                file.write(chunk)
        print(f"다운로드 완료: {gz_filename} → {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"다운로드 실패: {gz_filename} - {e}")
print("모든 파일 다운로드가 완료되었습니다.")