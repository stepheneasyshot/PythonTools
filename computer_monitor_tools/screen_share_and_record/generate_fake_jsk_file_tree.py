import os

# 定义文件树结构
# 字典的键是文件夹名，值是子文件夹的列表或字典。
# 如果是空列表，表示这是一个空文件夹。
# 如果是字典，表示有子文件夹。
# 也可以用None表示一个文件（虽然你的树里全是文件夹）。
file_tree = {
    'bin': {
        'server': {}
    },
    'conf': {
        'management': {},
        'security': {
            'policy': {
                'limited': {},
                'unlimited': {}
            }
        }
    },
    'demo': {
        'jfc': {
            'CodePointIM': {},
            'FileChooserDemo': {},
            'Font2DTest': {},
            'J2Ddemo': {},
            'Metalworks': {},
            'Notepad': {},
            'SampleTree': {},
            'Stylepad': {},
            'SwingSet2': {},
            'TableExample': {},
            'TransparentRuler': {}
        },
        'nbproject': {
            'jfc': {
                'FileChooserDemo': {'nbproject': {}},
                'Font2DTest': {'nbproject': {}},
                'Metalworks': {'nbproject': {}},
                'Notepad': {'nbproject': {}},
                'SampleTree': {'nbproject': {}},
                'SwingApplet': {'nbproject': {}},
                'TableExample': {'nbproject': {}},
                'TransparentRuler': {'nbproject': {}}
            },
            'management': {
                'FullThreadDump': {'nbproject': {}},
                'JTop': {'nbproject': {}},
                'MemoryMonitor': {'nbproject': {}},
                'VerboseGC': {'nbproject': {}}
            },
            'scripting': {
                'jconsole-plugin': {'nbproject': {}}
            }
        }
    },
    'include': {
        'win32': {
            'bridge': {}
        }
    },
    'jmods': {},
    'legal': {
        'com.azul.crs.client': {},
        'com.azul.tooling': {},
        'java.base': {},
        'java.compiler': {},
        'java.datatransfer': {},
        'java.desktop': {},
        'java.instrument': {},
        'java.logging': {},
        'java.management': {},
        'java.management.rmi': {},
        'java.naming': {},
        'java.net.http': {},
        'java.prefs': {},
        'java.rmi': {},
        'java.scripting': {},
        'java.se': {},
        'java.security.jgss': {},
        'java.security.sasl': {},
        'java.smartcardio': {},
        'java.sql': {},
        'java.sql.rowset': {},
        'java.transaction.xa': {},
        'java.xml': {},
        'java.xml.crypto': {},
        'jdk.accessibility': {},
        'jdk.aot': {},
        'jdk.attach': {},
        'jdk.charsets': {},
        'jdk.compiler': {},
        'jdk.crypto.cryptoki': {},
        'jdk.crypto.ec': {},
        'jdk.crypto.mscapi': {},
        'jdk.dynalink': {},
        'jdk.editpad': {},
        'jdk.hotspot.agent': {},
        'jdk.httpserver': {},
        'jdk.internal.ed': {},
        'jdk.internal.jvmstat': {},
        'jdk.internal.le': {},
        'jdk.internal.opt': {},
        'jdk.internal.vm.ci': {},
        'jdk.internal.vm.compiler': {},
        'jdk.internal.vm.compiler.management': {},
        'jdk.jartool': {},
        'jdk.javadoc': {},
        'jdk.jcmd': {},
        'jdk.jconsole': {},
        'jdk.jdeps': {},
        'jdk.jdi': {},
        'jdk.jdwp.agent': {},
        'jdk.jfr': {},
        'jdk.jlink': {},
        'jdk.jshell': {},
        'jdk.jsobject': {},
        'jdk.jstatd': {},
        'jdk.localedata': {},
        'jdk.management': {},
        'jdk.management.agent': {},
        'jdk.management.jfr': {},
        'jdk.naming.dns': {},
        'jdk.naming.ldap': {},
        'jdk.naming.rmi': {},
        'jdk.net': {},
        'jdk.pack': {},
        'jdk.rmic': {},
        'jdk.scripting.nashorn': {},
        'jdk.scripting.nashorn.shell': {},
        'jdk.sctp': {},
        'jdk.security.auth': {},
        'jdk.security.jgss': {},
        'jdk.unsupported': {},
        'jdk.unsupported.desktop': {},
        'jdk.xml.dom': {},
        'jdk.zipfs': {}
    },
    'lib': {
        'jfr': {},
        'security': {},
        'server': {}
    }
}


def create_directory_tree(base_path, tree_dict):
    """
    递归地创建文件树。

    Args:
        base_path (str): 当前要创建文件夹的根路径。
        tree_dict (dict): 当前级别的文件夹字典。
    """
    for folder_name, sub_tree in tree_dict.items():
        # 构建新的路径
        new_path = os.path.join(base_path, folder_name)

        # 创建文件夹
        try:
            os.makedirs(new_path, exist_ok=True)
            print(f"创建目录: {new_path}")
        except OSError as e:
            print(f"无法创建目录 {new_path}: {e}")
            continue

        # 如果有子目录，则递归调用
        if sub_tree:
            create_directory_tree(new_path, sub_tree)


def generate_tree(path):
    # 定义基础目录，你可以在这里修改它
    base_dir = path

    # 确保基础目录存在
    os.makedirs(base_dir, exist_ok=True)

    # 开始创建文件树
    print(f"开始在 '{os.path.abspath(base_dir)}' 目录下创建文件树...")
    create_directory_tree(base_dir, file_tree)
    print("文件树创建完成。")