"use strict";
(self["webpackChunkjupyterlab_bxplorer_v2"] = self["webpackChunkjupyterlab_bxplorer_v2"] || []).push([["lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4"],{

/***/ "./lib/components/BasicTabs.js":
/*!*************************************!*\
  !*** ./lib/components/BasicTabs.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Tabs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/Tabs */ "./node_modules/@mui/material/esm/Tabs/Tabs.js");
/* harmony import */ var _mui_material_Tab__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Tab */ "./node_modules/@mui/material/esm/Tab/Tab.js");
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/esm/Box/Box.js");
/* harmony import */ var _CustomTabPanel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./CustomTabPanel */ "./lib/components/CustomTabPanel.js");
/* harmony import */ var _FMViewComponent__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./FMViewComponent */ "./lib/components/FMViewComponent.js");






const BasicTabs = (props) => {
    const [value, setValue] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(0);
    const handleChange = (event, newValue) => {
        setValue(newValue);
    };
    const a11yProps = (index) => ({
        id: `simple-tab-${index}`,
        'aria-controls': `simple-tabpanel-${index}`,
    });
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { width: '100%' } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { borderBottom: 1, borderColor: 'divider' } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Tabs__WEBPACK_IMPORTED_MODULE_2__["default"], { value: value, onChange: handleChange, "aria-label": "basic tabs example" },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Tab__WEBPACK_IMPORTED_MODULE_3__["default"], { label: "Private", ...a11yProps(0) }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Tab__WEBPACK_IMPORTED_MODULE_3__["default"], { label: "Public", ...a11yProps(1) }))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CustomTabPanel__WEBPACK_IMPORTED_MODULE_4__["default"], { value: value, index: 0 },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_FMViewComponent__WEBPACK_IMPORTED_MODULE_5__["default"], { downloadsFolder: props.downloadsFolder, clientType: "private" })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CustomTabPanel__WEBPACK_IMPORTED_MODULE_4__["default"], { value: value, index: 1 },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_FMViewComponent__WEBPACK_IMPORTED_MODULE_5__["default"], { downloadsFolder: props.downloadsFolder, clientType: "public" }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (BasicTabs);


/***/ }),

/***/ "./lib/components/CustomTabPanel.js":
/*!******************************************!*\
  !*** ./lib/components/CustomTabPanel.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/esm/Box/Box.js");


const CustomTabPanel = (props) => {
    const { children, value, index, ...other } = props;
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { role: "tabpanel", hidden: value !== index, id: `simple-tabpanel-${index}`, "aria-labelledby": `simple-tab-${index}`, ...other, style: { height: "calc(100vh - 48px)" } }, value === index && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_1__["default"], { sx: { p: 3, height: "100%", overflowY: "auto" } }, children))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (CustomTabPanel);


/***/ }),

/***/ "./lib/components/FMViewComponent.js":
/*!*******************************************!*\
  !*** ./lib/components/FMViewComponent.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @syncfusion/ej2-react-filemanager */ "webpack/sharing/consume/default/@syncfusion/ej2-react-filemanager/@syncfusion/ej2-react-filemanager");
/* harmony import */ var _syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);




const FMViewComponent = (props) => {
    const downloadsFolder = props.downloadsFolder || "downloads";
    const clientType = props.clientType || "private";
    const fileManagerRef = (0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);
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
    const ajaxSettings = {
        url: backendUrl + "/jupyterlab-bxplorer-v2/FileOperations",
    };
    function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return match ? match[2] : null;
    }
    // Evento para inyectar client_type en cada solicitud AJAX del FileManager.
    const onBeforeSend = (args) => {
        if (args.ajaxSettings) {
            const xsrfToken = getCookie('_xsrf');
            args.ajaxSettings.beforeSend = function (args) {
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
            }
            catch (e) {
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
    const contextMenuClickHandler = (args) => {
        console.log("menuClick args:", args);
        if (args.item && args.item.text === "Download") {
            args.cancel = true;
            const currentPath = fileManagerRef.current.path || "/";
            const selectedItems = args.data || (fileManagerRef.current && fileManagerRef.current.selectedItems);
            if (!selectedItems || selectedItems.length === 0) {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: 'Información',
                    body: 'No se ha seleccionado ningún archivo',
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: 'Aceptar' })]
                });
                return;
            }
            // Construimos la estructura de datos que espera el backend, agregando client_type.
            const payloadObj = {
                action: "download",
                path: currentPath,
                downloadsFolder: downloadsFolder,
                client_type: clientType,
                names: selectedItems.map((item) => item.name || item),
                data: selectedItems.map((item) => {
                    if (typeof item === "string") {
                        return {
                            name: item,
                            isFile: true,
                            path: currentPath.endsWith("/")
                                ? currentPath + item
                                : currentPath + "/" + item,
                        };
                    }
                    else {
                        return item;
                    }
                }),
            };
            const payload = JSON.stringify(payloadObj);
            const formData = new URLSearchParams();
            formData.append("downloadInput", payload);
            (0,_handler__WEBPACK_IMPORTED_MODULE_3__.requestAPI)('FileOperations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData.toString(),
            })
                .then((data) => {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: 'Operación exitosa',
                    body: `Archivo guardado en: ${data.file_saved}`,
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.Dialog.okButton({ label: 'Aceptar' })]
                });
            })
                .catch((error) => {
                console.error("Error en la descarga:", error);
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)('Error en la descarga', 'Ocurrió un error al descargar el archivo.');
            });
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "control-section", style: { height: "100%" } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__.FileManagerComponent, { ref: fileManagerRef, id: "file", ajaxSettings: ajaxSettings, beforeSend: onBeforeSend.bind(undefined), toolbarSettings: {
                items: ['SortBy', 'Refresh'],
                visible: true,
            }, contextMenuSettings: {
                file: ['Download', '|', 'Details'],
                folder: ['Open', '|', 'Details'],
                layout: [],
                visible: true,
            }, detailsViewSettings: {
                columns: [
                    { field: "name", headerText: "Name", minWidth: 120, width: "auto" },
                    { field: "region", headerText: "Region", minWidth: 100, width: "120px" },
                    { field: "dateModified", headerText: "Modified", minWidth: 120, width: "150px" },
                    { field: "size", headerText: "Size", minWidth: 80, width: "100px" },
                ],
            }, view: "Details", allowMultiSelection: false, height: "100%" // O puedes usar style={{ height: "100%" }}
            , ...{ menuClick: contextMenuClickHandler } },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__.Inject, { services: [_syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__.DetailsView, _syncfusion_ej2_react_filemanager__WEBPACK_IMPORTED_MODULE_1__.Toolbar] }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (FMViewComponent);


/***/ }),

/***/ "./lib/components/FileManagerPanelComponent.js":
/*!*****************************************************!*\
  !*** ./lib/components/FileManagerPanelComponent.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _BasicTabs__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./BasicTabs */ "./lib/components/BasicTabs.js");
// import { AppBar, Container, CssBaseline, IconButton, Toolbar, Typography } from '@mui/material'
// import Refresh from '@mui/icons-material/Refresh';
// import Close from '@mui/icons-material/Close';


const FileManagerPanelComponent = (props) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: { width: "100%", minWidth: "400px", height: "100vh" } },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_BasicTabs__WEBPACK_IMPORTED_MODULE_1__["default"], { downloadsFolder: props.downloadsFolder })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (FileManagerPanelComponent);


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-bxplorer-v2', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widgets_FileManagerPanelWidget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widgets/FileManagerPanelWidget */ "./lib/widgets/FileManagerPanelWidget.js");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _syncfusion_ej2_base__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @syncfusion/ej2-base */ "./node_modules/@syncfusion/ej2-base/index.js");





// Registering Syncfusion<sup style="font-size:70%">&reg;</sup> license key
(0,_syncfusion_ej2_base__WEBPACK_IMPORTED_MODULE_3__.registerLicense)('Ngo9BigBOggjHTQxAR8/V1NNaF5cXmBCf1FpRmJGdld5fUVHYVZUTXxaS00DNHVRdkdmWXxcd3VcRmBeVkd+W0VWYUA=');
const PLUGIN_ID = 'jupyterlab-bxplorer-v2:plugin';
async function activate(app, settingRegistry) {
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
            downloadsFolder = settings.get('download-folder').composite || "";
            console.log('downloadsFolder:', downloadsFolder);
        })
            .catch(reason => {
            console.error('Failed to load settings for jupyterlab-bxplorer-v2.', reason);
        });
    }
    const sideBarContent = new _widgets_FileManagerPanelWidget__WEBPACK_IMPORTED_MODULE_4__.FileManagerPanelWidget(downloadsFolder);
    const sideBarWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
        content: sideBarContent
    });
    sideBarWidget.toolbar.hide();
    sideBarWidget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.runIcon;
    sideBarWidget.title.caption = 'File Manager';
    app.shell.add(sideBarWidget, 'left', { rank: 501 });
}
/**
 * Initialization data for the jupyterlab-bxplorer-v2 extension.
 */
const plugin = {
    id: PLUGIN_ID,
    description: 'A JupyterLab extension.',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry],
    activate
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/widgets/FileManagerPanelWidget.js":
/*!***********************************************!*\
  !*** ./lib/widgets/FileManagerPanelWidget.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   FileManagerPanelWidget: () => (/* binding */ FileManagerPanelWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_FileManagerPanelComponent__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/FileManagerPanelComponent */ "./lib/components/FileManagerPanelComponent.js");



class FileManagerPanelWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(downloadsFolder) {
        super();
        this.downloadsFolder = downloadsFolder;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { style: {
                width: '100%',
            } },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_components_FileManagerPanelComponent__WEBPACK_IMPORTED_MODULE_2__["default"], { downloadsFolder: this.downloadsFolder })));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_cons-092fe4.7cd66ff0c711e724d8db.js.map