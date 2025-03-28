import os

from kabaret import flow
from kabaret.flow.object import _Manager

from libreflow.baseflow.file import GenericRunAction,TrackedFile,TrackedFolder,FileRevisionNameChoiceValue

class ExportPSDLayers(GenericRunAction):
    _MANAGER_TYPE = _Manager

    ICON = ('icons.flow', 'photoshop')

    _file = flow.Parent()
    _files = flow.Parent(2)
    _task = flow.Parent(3)
    _shot = flow.Parent(5)
    _sequence = flow.Parent(7)

    revision = flow.Param(None, FileRevisionNameChoiceValue)

    exec_path = ""

    def allow_context(self, context):
        return (
            context
            and self._file.format.get() in ['psd', 'psb']
            )

    def needs_dialog(self):
        return True

    def get_buttons(self):
        self.revision.revert_to_default()

        msg = ""

        site_env = self.root().project().get_current_site().site_environment
        if site_env.has_mapped_name('PHOTOSHOP_EXEC_PATH'):
            self.exec_path = site_env['PHOTOSHOP_EXEC_PATH'].value.get()
            self.message.set(msg)
            return ['Export','Cancel']

        else :
            msg = "<font color = red><b>Photoshop executable not found in site environment</b></font>"
            self.message.set(msg)
            return ['Cancel']
    
    def ensure_render_folder(self):
        folder_name = self._file.display_name.get().split('.')[0]
        folder_name += '_render'

        if not self._files.has_folder(folder_name):
            self._files.create_folder_action.folder_name.set(folder_name)
            self._files.create_folder_action.category.set('Outputs')
            self._files.create_folder_action.tracked.set(True)
            self._files.create_folder_action.run(None)
        
        return self._files[folder_name]
    
    def ensure_render_folder_revision(self):
        folder = self.ensure_render_folder()
        revision_name = self.revision.get()
        revisions = folder.get_revisions()
        source_revision = self._file.get_revision(self.revision.get())
        
        if not folder.has_revision(revision_name):
            revision = folder.add_revision(revision_name)
            folder.set_current_user_on_revision(revision_name)
        else:
            revision = folder.get_revision(revision_name)
        
        revision.comment.set(source_revision.comment.get())
        
        folder.ensure_last_revision_oid()
        
        self._files.touch()
        
        return revision
    
    def runner_name_and_tags(self):
        return 'Photoshop', []
    
    def get_run_label(self):
        return 'Export Layers'

    def target_file_extension(self):
        if self._file.format.get() == 'psb':
            return 'psb'
        elif self._file.format.get() == 'psd':
            return 'psd'

    def extra_argv(self):
        rev = self._file.get_revision(self.revision.get())
        current_dir = os.path.split(__file__)[0]
        script_path = os.path.normpath(os.path.join(current_dir,"scripts/LFS_PSD_export_to_PNG.jsx"))

        return [rev.get_path(),script_path]
    
    def run(self, button):
        if button == 'Cancel':
            return

        folder_path = self.ensure_render_folder_revision().get_path()

        super(ExportPSDLayers, self).run(button)
        return self.get_result(close=True)


def export_psd_layers(parent):
    if isinstance(parent, TrackedFile):
        r = flow.Child(ExportPSDLayers)
        r.name = 'export_layers'
        return r


def install_extensions(session):
    return {
        "export_psd_layers": [
            export_psd_layers,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
