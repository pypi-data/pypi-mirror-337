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

  const getBaseUrl = () => {
    const pathParts = window.location.pathname.split("/");
    // Encontrar el índice donde aparece "user"
    const userIndex = pathParts.indexOf("user");

    if (userIndex !== -1 && pathParts.length > userIndex + 1) {
      // Construir la base URL hasta el nombre del usuario
      return `${window.location.origin}/user/${pathParts[userIndex + 1]}`;
    }

    // Si no se detecta el formato esperado, retornar solo el origen
    return window.location.origin;
  };

  // Generar la URL para el servicio backend
  const backendUrl = getBaseUrl();

  console.log(backendUrl);

  // const hostUrl = "https://demo.opensciencestudio.com/user/lleon"
  const ajaxSettings: object = {
    url: backendUrl + "/jupyterlab-bxplorer-v2/FileOperations",
  };


  function getCookie(name: any) {
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    return match ? match[2] : null;
  }

  // Evento para inyectar client_type en cada solicitud AJAX del FileManager.
  const onBeforeSend = (args: any): void => {
    if (args.ajaxSettings) {

      const xsrfToken = getCookie('_xsrf');
      args.ajaxSettings.beforeSend = function (args: any) {
        args.httpRequest.setRequestHeader("X-XSRFToken", xsrfToken);
      };
    }
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

  // const onBeforeSend = (args: any): void => {
  //   console.log("ajaxBeforeSend action:", args.action);
  //   // Cancel the default AJAX call
  //   args.cancel = true;

  //   let currentData = args.ajaxSettings.data;
  //   if (typeof currentData === "string") {
  //     try {
  //       currentData = JSON.parse(currentData);
  //     } catch (e) {
  //       console.error("Error parsing ajaxSettings.data:", e);
  //       currentData = {};
  //     }
  //   }

  //   // Inject the client_type property
  //   const modifiedData = { ...currentData, client_type: clientType };

  //   requestAPI('FileOperations', {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify(modifiedData)
  //   })
  //     .then((result: any) => {
  //       console.log("Result from requestAPI:", result);
  //       // If the backend response is wrapped in a 'data' property, extract it.
  //       let responseData = result;
  //       if (result && result.data) {
  //         responseData = result.data;
  //       }
  //       // Verify that the response contains the expected keys.
  //       if (!responseData.cwd || !responseData.files) {
  //         console.error("Unexpected response structure:", responseData);
  //       }
  //       // Pass the response along with the original args
  //       if (args.onSuccess) {
  //         args.onSuccess(responseData, args);
  //       }
  //     })
  //     .catch((err: any) => {
  //       console.error("Error in requestAPI:", err);
  //       if (args.onFailure) {
  //         args.onFailure(err, args);
  //       }
  //     });
  // };

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
