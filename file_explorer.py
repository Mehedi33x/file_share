from flask import Flask, request, redirect, render_template_string, send_from_directory, send_file, session
import os
import zipfile
import tempfile
import getpass  # For secure password input
app = Flask(__name__)
app.secret_key = "super_secret_key_123"
# ====================== DYNAMIC LOGIN SETUP ======================
def setup_credentials():
    print("\n" + "="*50)
    print("🔐 SECURE FILE EXPLORER - CREDENTIAL SETUP")
    print("="*50)
    username = input("Enter Username: ").strip()
    while True:
        password = getpass.getpass("Enter Password: ")
        confirm = getpass.getpass("Confirm Password: ")
        if password == confirm:
            print("✅ Credentials set successfully!\n")
            break
        else:
            print("❌ Passwords do not match. Please try again.\n")
    return username, password
# Setup credentials when the app starts
USERNAME, PASSWORD = setup_credentials()
ALLOWED_PATHS = [
    os.path.expanduser("~/Downloads"),
    "D:\\",
    "E:\\"
]
# ====================== SECURITY ======================
def is_allowed(path):
    try:
        path = os.path.abspath(path)
        return any(path.startswith(os.path.abspath(p)) for p in ALLOWED_PATHS)
    except:
        return False
def zip_folder(folder_path):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    with zipfile.ZipFile(temp.name, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full = os.path.join(root, file)
                arc = os.path.relpath(full, folder_path)
                z.write(full, arc)
    return temp.name
# ====================== IMPROVED LOGIN UI WITH ERROR MESSAGE ======================
LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style> 
        body { font-family: 'Segoe UI', system-ui, sans-serif; } 
    </style>
</head>
<body class="bg-gradient-to-br from-gray-950 to-gray-900 flex items-center justify-center min-h-screen text-white">
    <div class="bg-gray-900/80 backdrop-blur-xl p-10 rounded-3xl w-full max-w-md shadow-2xl border border-gray-700">
        <div class="text-center mb-8">
            <div class="inline-flex items-center justify-center w-20 h-20 bg-blue-600 rounded-2xl mb-4">
                <i class="fa-solid fa-folder-open text-4xl"></i>
            </div>
            <h1 class="text-3xl font-bold">Secure File Explorer</h1>
            <p class="text-gray-400 mt-2">Access your files safely</p>
        </div>
        {% if error %}
        <div class="bg-red-500/10 border border-red-500 text-red-400 px-4 py-3 rounded-2xl mb-6 flex items-center gap-3">
            <i class="fa-solid fa-circle-exclamation"></i>
            <span>{{ error }}</span>
        </div>
        {% endif %}
        <form method="POST" class="space-y-6">
            <div>
                <label class="block text-sm text-gray-400 mb-1.5">Username</label>
                <div class="relative">
                    <div class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
                        <i class="fa-solid fa-user"></i>
                    </div>
                    <input name="username" placeholder="Enter username" value="{{ username|default('') }}"
                           class="w-full pl-11 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-2xl focus:outline-none focus:border-blue-500 transition-colors">
                </div>
            </div>
            <div>
                <label class="block text-sm text-gray-400 mb-1.5">Password</label>
                <div class="relative">
                    <div class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
                        <i class="fa-solid fa-lock"></i>
                    </div>
                    <input name="password" type="password" placeholder="Enter password"
                           class="w-full pl-11 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-2xl focus:outline-none focus:border-blue-500 transition-colors">
                </div>
            </div>
            <button type="submit"
                    class="w-full bg-blue-600 hover:bg-blue-700 transition-all py-4 rounded-2xl font-semibold text-lg flex items-center justify-center gap-2">
                <i class="fa-solid fa-right-to-bracket"></i>
                Login
            </button>
        </form>
    </div>
</body>
</html>
"""
# ====================== UPDATED LOGIN ROUTE ======================
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    username_value = ""
    if request.method == "POST":
        submitted_username = request.form.get("username", "").strip()
        submitted_password = request.form.get("password", "")
        if submitted_username == USERNAME and submitted_password == PASSWORD:
            session["user"] = True
            return redirect("/files")
        else:
            error = "❌ Incorrect username or password. Please try again."
            username_value = submitted_username   # Keep username so user doesn't have to retype
    return render_template_string(LOGIN_PAGE, 
                                  error=error, 
                                  username=username_value)
# ====================== IMPROVED FILE UI (Same as before) ======================
FILE_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        body { font-family: 'Segoe UI', system-ui, sans-serif; }
        .file-card:hover { 
            transform: translateY(-4px); 
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.3);
        }
    </style>
</head>
<body class="bg-gray-950 text-white min-h-screen">
    <div class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div class="flex justify-between items-center px-8 py-5">
            <div class="flex items-center gap-4">
                <i class="fa-solid fa-folder-tree text-3xl text-blue-500"></i>
                <h1 class="text-2xl font-bold">File Explorer</h1>
            </div>
            <a href="/logout" 
               class="flex items-center gap-2 bg-red-600 hover:bg-red-700 px-6 py-3 rounded-2xl transition-all font-medium">
                <i class="fa-solid fa-right-from-bracket"></i>
                <span>Logout</span>
            </a>
        </div>
    </div>
    <div class="p-8 max-w-7xl mx-auto">
        <div class="flex items-center gap-3 bg-gray-900 p-5 rounded-3xl mb-8 border border-gray-800">
            <i class="fa-solid fa-location-dot text-blue-400"></i>
            <p class="text-gray-300 font-medium break-all text-lg">{{ path }}</p>
        </div>
        <div class="flex gap-4 mb-10">
            <a href="/zip?path={{ path }}" 
               class="flex items-center gap-3 bg-emerald-600 hover:bg-emerald-700 transition-all px-7 py-4 rounded-3xl font-semibold shadow-lg">
                <i class="fa-solid fa-file-zipper text-xl"></i>
                Download Folder as ZIP
            </a>
        </div>
        <div class="mb-12">
            <h2 class="flex items-center gap-3 text-2xl font-semibold text-emerald-400 mb-6">
                <i class="fa-solid fa-folder"></i>
                Folders ({{ folders|length }})
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
                {% for f in folders %}
                <a href="/files?path={{ path }}/{{ f }}" 
                   class="file-card group bg-gray-900 hover:bg-gray-800 border border-gray-700 hover:border-emerald-500 p-6 rounded-3xl transition-all duration-300">
                    <div class="text-6xl mb-4 text-emerald-400 group-hover:scale-110 transition-transform">📁</div>
                    <p class="font-semibold text-lg truncate">{{ f }}</p>
                </a>
                {% endfor %}
            </div>
        </div>
        <div>
            <h2 class="flex items-center gap-3 text-2xl font-semibold text-sky-400 mb-6">
                <i class="fa-solid fa-file"></i>
                Files ({{ files|length }})
            </h2>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
                {% for f in files %}
                <a href="/download?path={{ path }}&file={{ f }}" 
                   class="file-card group bg-gray-900 hover:bg-gray-800 border border-gray-700 hover:border-sky-500 p-6 rounded-3xl transition-all duration-300">
                    <div class="text-6xl mb-4 text-sky-400 group-hover:scale-110 transition-transform">📄</div>
                    <p class="font-semibold text-lg truncate">{{ f }}</p>
                </a>
                {% endfor %}
            </div>
        </div>
        {% if not folders and not files %}
        <div class="text-center py-24 text-gray-500">
            <i class="fa-solid fa-folder-open text-7xl mb-6 opacity-50"></i>
            <p class="text-2xl font-medium">This folder is empty</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""
# ====================== INITIAL LOCATION PAGE ======================
INITIAL_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style> body { font-family: 'Segoe UI', system-ui, sans-serif; } </style>
</head>
<body class="bg-gray-950 text-white min-h-screen">
    <div class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div class="flex justify-between items-center px-8 py-5">
            <div class="flex items-center gap-4">
                <i class="fa-solid fa-folder-tree text-3xl text-blue-500"></i>
                <h1 class="text-2xl font-bold">File Explorer</h1>
            </div>
            <a href="/logout" class="flex items-center gap-2 bg-red-600 hover:bg-red-700 px-6 py-3 rounded-2xl transition-all font-medium">
                <i class="fa-solid fa-right-from-bracket"></i>
                <span>Logout</span>
            </a>
        </div>
    </div>
    <div class="p-8 max-w-4xl mx-auto">
        <div class="text-center mb-10">
            <h2 class="text-3xl font-bold mb-3">Choose Starting Location</h2>
            <p class="text-gray-400">Select a folder to begin exploring</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <a href="/files?path=~/Downloads" class="bg-gray-900 hover:bg-gray-800 border border-gray-700 hover:border-blue-500 p-8 rounded-3xl transition-all group">
                <div class="text-6xl mb-6">📥</div>
                <h3 class="text-2xl font-semibold mb-2">Downloads</h3>
                <p class="text-gray-500">Your downloaded files</p>
            </a>
            <a href="/files?path=D:\\" class="bg-gray-900 hover:bg-gray-800 border border-gray-700 hover:border-blue-500 p-8 rounded-3xl transition-all group">
                <div class="text-6xl mb-6">💾</div>
                <h3 class="text-2xl font-semibold mb-2">D: Drive</h3>
                <p class="text-gray-500">Local Disk D</p>
            </a>
            <a href="/files?path=E:\\" class="bg-gray-900 hover:bg-gray-800 border border-gray-700 hover:border-blue-500 p-8 rounded-3xl transition-all group">
                <div class="text-6xl mb-6">💾</div>
                <h3 class="text-2xl font-semibold mb-2">E: Drive</h3>
                <p class="text-gray-500">Local Disk E</p>
            </a>
        </div>
    </div>
</body>
</html>
"""
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/files")
def files():
    if not session.get("user"):
        return redirect("/")
    path = request.args.get("path")
    if not path:
        return INITIAL_PAGE
    path = os.path.expanduser(path)
    if not is_allowed(path):
        return "⛔ Access denied"
    try:
        items = os.listdir(path)
        folders = [f for f in items if os.path.isdir(os.path.join(path, f))]
        files = [f for f in items if os.path.isfile(os.path.join(path, f))]
    except Exception:
        folders, files = [], []
    return render_template_string(FILE_PAGE, path=path, folders=folders, files=files)
@app.route("/download")
def download():
    if not session.get("user"):
        return redirect("/")
    path = request.args.get("path")
    file = request.args.get("file")
    if not is_allowed(path):
        return "⛔ Access denied"
    return send_from_directory(path, file, as_attachment=True)
@app.route("/zip")
def zip_download():
    if not session.get("user"):
        return redirect("/")
    path = request.args.get("path")
    if not is_allowed(path):
        return "⛔ Access denied"
    zip_path = zip_folder(path)
    return send_file(zip_path, as_attachment=True, download_name="folder_download.zip")
if __name__ == "__main__":
    print("🚀 Starting Secure File Explorer...")
    app.run(host="0.0.0.0", port=8000, debug=True)