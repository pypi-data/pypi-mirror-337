import os
import json
import subprocess

from kabaret import flow
from kabaret.flow.object import _Manager
from libreflow.baseflow.file import GenericRunAction, TrackedFile, TrackedFolder
from libreflow.baseflow.task import Task

class CreateTvPaintFile(flow.Action):
    
    _task = flow.Parent()
    _tasks = flow.Parent(2)
    _shot = flow.Parent(3)
    _sequence = flow.Parent(5)
    _layout_source_path = flow.Computed(cached=True)
    _color_source_path = flow.Computed(cached=True)

    def allow_context(self, context):
        return context

    def needs_dialog(self):
        self._layout_source_path.touch()
        self._color_source_path.touch()

        if (self._layout_source_path.get() is None):
            self.message.set('<font color=orange>BG Layout layer folder not found</font>')
            return True

        if (self._color_source_path.get() is None):
            self.message.set('<font color=orange>BG Color layer folder not found</font>')
            return True

        return False
    
    def get_buttons(self):
        return ['Close']
    
    def check_tvpaint_running(self):
        # Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if "tvpaint animation" in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        return False

    def compute_child_value(self, child_value):
        if child_value is self._layout_source_path:
            self._layout_source_path.set(self.get_source_path('bg_layout'))
        elif child_value is self._color_source_path:
            self._color_source_path.set(self.get_source_path('bg_color'))

    def get_file(self, task_name, file_name):
        if not self._tasks.has_mapped_name(task_name):
            return None
        task = self._tasks[task_name]

        name, ext = os.path.splitext(file_name)
        if task.files.has_file(name, ext[1:]):
            file_name = "%s_%s" % (name, ext[1:])
            return task.files[file_name]
        
        return None

    def start_tvpaint(self,path):
        start_action = self._task.start_tvpaint
        start_action.file_path.set(path)
        start_action.run(None)

    def execute_create_tvpaint_script(self, layout_path, color_path,width=None,height=None):
        exec_script = self._task.execute_create_tvpaint_script
        exec_script._layout_source_path.set(layout_path)
        exec_script._color_source_path.set(color_path)
        exec_script.width.set(width)
        exec_script.height.set(height)
        exec_script.run(None)
    
    def get_default_file(self, task_name, file_name):
        file_mapped_name = file_name.replace('.', '_')
        mng = self.root().project().get_task_manager()

        dft_task = mng.default_tasks[task_name]
        if not dft_task.files.has_mapped_name(file_mapped_name): # check default file
            # print(f'Scene Builder - default task {task_name} has no default file {filename} -> use default template')
            return None

        dft_file = dft_task.files[file_mapped_name]
        return dft_file

    def get_source_path(self,task_name):
        if not self._shot.tasks.has_mapped_name(task_name):
            return None
        self.source_task = self._shot.tasks[task_name]
        print('source task : ', self.source_task.name())
        
        if not self.source_task.files.has_folder(task_name + '_render'):
            return None
        f = self.source_task.files[f'{task_name}_render']
        print('source folder : ', f.name())
        
        rev = f.get_head_revision(sync_status="Available")
        if rev is None:
            return None
        print ('source rev : ', rev.name())

        path = rev.get_path()
        print ('source rev path : ', path, os.path.isdir(path))
        return path if os.path.isdir(path) else None
    
    def get_first_image_resolution(self,folder_path):

        folder_content = os.listdir(folder_path)

        img_path = None

        for file in folder_content:
            img_path = os.path.join(folder_path,file)
            if os.path.splitext(img_path)[1] == '.png':
                break

        check_res = subprocess.check_output(f'identify -ping -format "%wx%h" "{img_path}"', shell=True).decode()
            
        res = check_res.split('x')

        return res

    def _ensure_file(self, name, format, path_format):

        files = self._task.files
        file_name = "%s_%s" % (name, format)

        if files.has_file(name, format):
            file = files[file_name]
        else:
            file = files.add_file(
                name=name,
                extension=format,
                tracked=True,
                default_path_format=path_format,
            )

        revision = file.create_working_copy()

        file.file_type.set('Works')

        return revision.get_path()

    def run(self,button):
        if button == 'Close':
            return
        

        path_format = None
        task_name = self._task.name()
        default_file = self.get_default_file(task_name, f"{task_name}.tvpp")
        if default_file is not None:
            path_format = default_file.path_format.get()
        anim_path = self._ensure_file(
            name=task_name,
            format="tvpp",
            path_format=path_format
        )

        # if self.check_tvpaint_running() is False:
        #     print(anim_path)
        self.start_tvpaint(anim_path)
        

        # Get TVPaint file
        tvpaint_file = self.get_file(self._task.name(), f"{self._task.name()}.tvpp")

        layout_res = self.get_first_image_resolution(self._layout_source_path.get())
        print('layout bg image resolution is: ', layout_res)

        color_res = self.get_first_image_resolution(self._color_source_path.get())
        print('color bg image resolution is: ', color_res)

        if color_res != layout_res :
            self.root().session().log_warning("Layout BG and Color BG are not corresponding, TvPaint Project will inherit Layout BG image size")

        self.execute_create_tvpaint_script(self._layout_source_path.get(), self._color_source_path.get(), layout_res[0], layout_res[1])

class StartTvPaint(GenericRunAction):

    file_path = flow.Param()

    def allow_context(self, context):
        return context

    def runner_name_and_tags(self):
        return 'TvPaint', []

    def target_file_extension(self):
        return 'tvpp'

    def extra_argv(self):
        return [self.file_path.get()]


class ExecuteCreateTvPaintScript(GenericRunAction):

    _layout_source_path = flow.Param()
    _color_source_path = flow.Param()
    width = flow.Param()
    height = flow.Param()

    def allow_context(self, context):
        return context
    
    def runner_name_and_tags(self):
        return 'PythonRunner', []

    def get_version(self, button):
        return None

    def get_run_label(self):
        return "Create TvPaint Project"

    def extra_argv(self):
        current_dir = os.path.split(__file__)[0]
        script_path = os.path.normpath(os.path.join(current_dir,"scripts/import_layers.py"))
        return [
                script_path,
                '--layoutbg-path', self._layout_source_path.get(), 
                '--colorbg-path', self._color_source_path.get() ,
                '--width', self.width.get(), 
                '--height', self.height.get()
                ]


def create_from_layers(parent):
    if isinstance(parent, Task):
        r = flow.Child(CreateTvPaintFile)
        r.name = 'create_tv_paint_file'
        r.index = None
        return r

def start_tvpaint(parent):
    if isinstance(parent, Task):
        r = flow.Child(StartTvPaint)
        r.name = 'start_tvpaint'
        r.index = None
        r.ui(hidden=True)
        return r

def execute_create_tvpaint_script(parent):
    if isinstance(parent, Task):
        r = flow.Child(ExecuteCreateTvPaintScript)
        r.name = 'execute_create_tvpaint_script'
        r.index = None
        r.ui(hidden=True)
        return r


def install_extensions(session):
    return {
        "tvpaint_scene_builder": [
            create_from_layers,
            start_tvpaint,
            execute_create_tvpaint_script,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
