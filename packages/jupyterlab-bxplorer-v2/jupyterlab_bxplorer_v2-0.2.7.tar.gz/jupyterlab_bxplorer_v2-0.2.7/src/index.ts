import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { runIcon } from '@jupyterlab/ui-components';
import { MainAreaWidget } from '@jupyterlab/apputils';
import { FileManagerPanelWidget } from './widgets/FileManagerPanelWidget';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { registerLicense } from '@syncfusion/ej2-base';

// Registering Syncfusion<sup style="font-size:70%">&reg;</sup> license key
registerLicense('Ngo9BigBOggjHTQxAR8/V1NNaF5cXmBCf1FpRmJGdld5fUVHYVZUTXxaS00DNHVRdkdmWXxcd3VcRmBeVkd+W0VWYUA=');


const PLUGIN_ID = 'jupyterlab-bxplorer-v2:plugin';

async function activate(app: JupyterFrontEnd, settingRegistry: ISettingRegistry): Promise<void> {
  console.log('JupyterLab extension jupyterlab-bxplorer-v2 is activated!');

  // await Promise.all([settingRegistry.load(PLUGIN_ID)])
  //   .then(([setting]) => {
  //     console.log('jupyterlab-bxplorer-v2 settings loaded:', setting.composite);
  //     let downloadFolder = setting.get('download-folder').composite as string || "";
  //     console.log('downloadFolder:', downloadFolder);
  //   }).catch((reason) => {
  //     console.error('Failed to load settings for jupyterlab-bxplorer-v2.', reason);
  //   });

  let downloadsFolder = "";
  if (settingRegistry) {
    await settingRegistry
      .load(plugin.id)
      .then(settings => {
        console.log('jupyterlab-bxplorer-v2 settings loaded:', settings.composite);
        downloadsFolder = settings.get('download-folder').composite as string || "";
        console.log('downloadsFolder:', downloadsFolder);
      })
      .catch(reason => {
        console.error('Failed to load settings for jupyterlab-bxplorer-v2.', reason);
      });
  }

  const sideBarContent = new FileManagerPanelWidget(downloadsFolder);
  const sideBarWidget = new MainAreaWidget<FileManagerPanelWidget>({
    content: sideBarContent
  });
  sideBarWidget.toolbar.hide();
  sideBarWidget.title.icon = runIcon;
  sideBarWidget.title.caption = 'File Manager';
  app.shell.add(sideBarWidget, 'left', { rank: 501 });
}

/**
 * Initialization data for the jupyterlab-bxplorer-v2 extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  description: 'A JupyterLab extension.',
  autoStart: true,
  optional: [ISettingRegistry],
  activate
};

export default plugin;
