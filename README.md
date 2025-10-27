# QDOJ-upload
可以实现oj练习题从txt转变为官方格式的xml文档并自动上传
## 项目说明

### 文件格式要求
- 请务必确保你的题目 txt 文档 **符合上传的 XML 基础格式**  
- `txt2fps.py` 会检测标签并进行一些修正和补全，随后将文件转换为 XML 格式，并保存在当前目录下的 `fps_xml/` 文件夹内
<img width="690" height="251" src="https://github.com/user-attachments/assets/ec51c265-74f2-4dfe-8913-ef741421c648" />  

- 如果错误的格式过多
<img width="891" height="75" src="https://github.com/user-attachments/assets/f8bb74b3-5ee3-461b-b491-5c0673d21ed2" />


### 已有完整 XML
- 如果你的文件本身就是 **完整的 XML 格式**，可直接使用 `fps_upload.py` 实现自动上传  
- 注意：该脚本 **默认读取 `fps_xml/` 目录** 中的文件  
  若不想创建 `fps_xml/`，请通过以下参数指定目录：  
  ```bash
  python fps_upload.py --dir 完整路径 --host IP --session session
<img width="980" height="261" src="https://github.com/user-attachments/assets/7f6ec398-6b6d-4ef1-9474-5a2d2a004215" />

- --dir功能介绍
<img width="1695" height="159" src="https://github.com/user-attachments/assets/825c64c7-88f3-4fdd-99c2-797c5c9d2de4" />


