from flask import *
from api.calclate import radix_conversion

app = Flask(__name__)

radix_list=["bin","dec","hex"]

@app.route("/")
def index():
    return render_template('index.html')
 
@app.route("/calc", methods=['GET','POST'])
def calc():
    if request.method == 'GET':
        return render_template('calc.html', radix_list = radix_list)
    elif request.method == 'POST':
        radix_name = request.form['radix_name']
        radix_num = request.form['radix_num']
        if   radix_name == "bin":
            result = radix_conversion.bin_to_dec_hex(radix_num)
            return render_template('calc.html', base_radix=radix_num,conv1_radix=result[0],conv2_radix=result[1],base_name="bin",conv1_name="dec",conv2_name="hex", radix_list = radix_list)
        elif radix_name == "dec":
            result = radix_conversion.dec_to_bin_hex(radix_num)
            return render_template('calc.html', base_radix=radix_num,conv1_radix=result[0],conv2_radix=result[1],base_name="dec",conv1_name="bin",conv2_name="hex", radix_list = radix_list)
        elif radix_name == "hex":
            result = radix_conversion.hex_to_bin_dec(radix_num)
            return render_template('calc.html', base_radix=radix_num,conv1_radix=result[0],conv2_radix=result[1],base_name="hex",conv1_name="bin",conv2_name="dec", radix_list = radix_list)
        else:
            return render_template('calc.html',error=result)

if __name__ == '__main__':
    app.run()