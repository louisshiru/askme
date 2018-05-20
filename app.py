# -*- coding: UTF-8 -*-

from flask import Flask, request, render_template
import qrcode

app = Flask(__name__, template_folder='templates', static_folder = 'templates')

IP = 'https://3c1813ce.ngrok.io'

def GetQRcode():
    
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 6,
        border = 2,
    )

    target = IP + '/Askme'

    qr.add_data(target)

    target = qr.make(fit=True)

    target = qr.make_image()

    target.save("./templates/QRcode")


def getImage():

    imageHerf = 'http://1.bp.blogspot.com/-wQVcouxZQjM/UlwKx68gZlI/AAAAAAAABUU/LoIKRkrrOjk/s1600/figure1.jpg'
    imageSrc = 'http://1.bp.blogspot.com/-wQVcouxZQjM/UlwKx68gZlI/AAAAAAAABUU/LoIKRkrrOjk/s1600/figure1.jpg'

    return imageHerf, imageSrc;

@app.route('/Askme', methods=['POST', 'GET'])
def main():

    # 獲取 QRcode	
    if request.method == 'GET':
        GetQRcode()
        return render_template('myapp.html', NgrokIP = IP + '/Askme')

    # 獲取使用者輸入
    UserInput = request.form['UserInput']
        
    imageHerf, imageSrc = getImage()

    # 創建模板
    template = render_template(
        'myapp.html', 
        ServerOutput = UserInput, 
        NgrokIP = IP + '/Askme', 
        imageHerf = imageHerf,
        imageSrc = imageSrc,
    )

    # 回傳模板
    return template

if __name__ == '__main__':
	app.run(debug = True, port = 5000)
