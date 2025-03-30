import React, { useRef } from 'react';
import {
  FileManagerComponent,
  Inject,
  DetailsView,
  Toolbar,
} from '@syncfusion/ej2-react-filemanager';
import { requestAPI } from '../handler';
import { showDialog, Dialog, showErrorMessage } from '@jupyterlab/apputils';

interface FMViewComponentProps {
  downloadsFolder: string;
  clientType: string;
}

const FMViewComponent: React.FC<FMViewComponentProps> = (props): JSX.Element => {
  const downloadsFolder = props.downloadsFolder || "downloads";
  const clientType = props.clientType || "private";
  const fileManagerRef = useRef<FileManagerComponent>(null);
  const hostUrl: string = "http://localhost:8000/jupyterlab-bxplorer-v2";
  const ajaxSettings: object = {
    url: hostUrl + "/FileOperations",
  };

  // Evento para inyectar client_type en cada solicitud AJAX del FileManager.
  const onBeforeSend = (args: any): void => {
    console.log("ajaxBeforeSend action:", args.action);
    console.log("ajaxBeforeSend args:", args);
    let currentData = args.ajaxSettings.data;
    // Si currentData es un string, lo parseamos a objeto.
    if (typeof currentData === "string") {
      try {
        currentData = JSON.parse(currentData);
      } catch (e) {
        console.error("Error al parsear ajaxSettings.data:", e);
        currentData = {};
      }
    }
    // Fusionamos los datos y agregamos client_type
    const modifiedData = { ...currentData, client_type: clientType };
    // Convertimos nuevamente a cadena JSON
    args.ajaxSettings.data = JSON.stringify(modifiedData);
    console.log("ajaxBeforeSend modified args:", args);
  };


  const contextMenuClickHandler = (args: any): void => {
    console.log("menuClick args:", args);
    if (args.item && args.item.text === "Download") {
      args.cancel = true;
      const currentPath = (fileManagerRef.current as any).path || "/";
      const selectedItems = args.data || (fileManagerRef.current && (fileManagerRef.current as any).selectedItems);
      if (!selectedItems || selectedItems.length === 0) {
        showDialog({
          title: 'Información',
          body: 'No se ha seleccionado ningún archivo',
          buttons: [Dialog.okButton({ label: 'Aceptar' })]
        });
        return;
      }

      // Construimos la estructura de datos que espera el backend, agregando client_type.
      const payloadObj = {
        action: "download",
        path: currentPath,
        downloadsFolder: downloadsFolder,
        client_type: clientType,
        names: selectedItems.map((item: any) => item.name || item),
        data: selectedItems.map((item: any) => {
          if (typeof item === "string") {
            return {
              name: item,
              isFile: true,
              path: currentPath.endsWith("/")
                ? currentPath + item
                : currentPath + "/" + item,
            };
          } else {
            return item;
          }
        }),
      };

      const payload = JSON.stringify(payloadObj);
      const formData = new URLSearchParams();
      formData.append("downloadInput", payload);

      requestAPI('FileOperations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString(),
      })
        .then((data: any) => {
          showDialog({
            title: 'Operación exitosa',
            body: `Archivo guardado en: ${data.file_saved}`,
            buttons: [Dialog.okButton({ label: 'Aceptar' })]
          });
        })
        .catch((error: any) => {
          console.error("Error en la descarga:", error);
          showErrorMessage('Error en la descarga', 'Ocurrió un error al descargar el archivo.');
        });
    }
  };

  return (
    <div className="control-section" style={{ height: "100%" }}>
      <FileManagerComponent
        ref={fileManagerRef}
        id="file"
        ajaxSettings={ajaxSettings}
        beforeSend={onBeforeSend.bind(this)}
        toolbarSettings={{
          items: ['SortBy', 'Refresh'],
          visible: true,
        }}
        contextMenuSettings={{
          file: ['Download', '|', 'Details'],
          folder: ['Open', '|', 'Details'],
          layout: [],
          visible: true,
        }}
        detailsViewSettings={{
          columns: [
            { field: "name", headerText: "Name", minWidth: 120, width: "auto" },
            { field: "region", headerText: "Region", minWidth: 100, width: "120px" },
            { field: "dateModified", headerText: "Modified", minWidth: 120, width: "150px" },
            { field: "size", headerText: "Size", minWidth: 80, width: "100px" },
          ],
        }}
        view="Details"
        allowMultiSelection={false}
        height="100%"  // O puedes usar style={{ height: "100%" }}
        {...({ menuClick: contextMenuClickHandler } as any)}
      >
        <Inject services={[DetailsView, Toolbar]} />
      </FileManagerComponent>
    </div>
  );
};

export default FMViewComponent;
