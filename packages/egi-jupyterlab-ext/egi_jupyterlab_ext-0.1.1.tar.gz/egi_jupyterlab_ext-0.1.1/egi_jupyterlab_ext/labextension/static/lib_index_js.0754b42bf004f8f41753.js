"use strict";
(self["webpackChunkegi_jupyterlab_ext"] = self["webpackChunkegi_jupyterlab_ext"] || []).push([["lib_index_js"],{

/***/ "./lib/CreateChartDialog.js":
/*!**********************************!*\
  !*** ./lib/CreateChartDialog.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ CreateChartDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Button__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @mui/material/Button */ "./node_modules/@mui/material/Button/Button.js");
/* harmony import */ var _mui_material_TextField__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @mui/material/TextField */ "./node_modules/@mui/material/TextField/TextField.js");
/* harmony import */ var _mui_material_Dialog__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material/Dialog */ "./node_modules/@mui/material/Dialog/Dialog.js");
/* harmony import */ var _mui_material_DialogActions__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @mui/material/DialogActions */ "./node_modules/@mui/material/DialogActions/DialogActions.js");
/* harmony import */ var _mui_material_DialogContent__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/DialogContent */ "./node_modules/@mui/material/DialogContent/DialogContent.js");
/* harmony import */ var _mui_material_DialogContentText__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @mui/material/DialogContentText */ "./node_modules/@mui/material/DialogContentText/DialogContentText.js");
/* harmony import */ var _mui_material_DialogTitle__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/DialogTitle */ "./node_modules/@mui/material/DialogTitle/DialogTitle.js");
/* harmony import */ var _components_SelectComponent__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/SelectComponent */ "./lib/components/SelectComponent.js");









const URL_GRAFANA_KEY = 'url_grafana';
function CreateChartDialog({ open, handleClose, sendNewUrl }) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Dialog__WEBPACK_IMPORTED_MODULE_1__["default"], { open: open, onClose: (_e, reason) => {
                if (reason === 'backdropClick' || reason === 'escapeKeyDown') {
                    return;
                }
                else {
                    handleClose(false);
                }
            }, slotProps: {
                paper: {
                    component: 'form',
                    onSubmit: (event) => {
                        event.preventDefault();
                        const formData = new FormData(event.currentTarget);
                        const formJson = Object.fromEntries(formData.entries());
                        if (URL_GRAFANA_KEY in formJson) {
                            const url = formJson.url_grafana;
                            sendNewUrl(url);
                            handleClose(false);
                        }
                        else {
                            throw 'Some error happened with the form.';
                        }
                    }
                }
            } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_DialogTitle__WEBPACK_IMPORTED_MODULE_2__["default"], null, "Subscribe"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_DialogContent__WEBPACK_IMPORTED_MODULE_3__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_DialogContentText__WEBPACK_IMPORTED_MODULE_4__["default"], null, "To create a chart, you must provide the URL from the Grafana's dashboard."),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_TextField__WEBPACK_IMPORTED_MODULE_5__["default"], { autoFocus: true, required: true, margin: "dense", id: "name", name: URL_GRAFANA_KEY, label: "Grafana URL", type: "url", fullWidth: true, variant: "outlined", size: "small" }),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_components_SelectComponent__WEBPACK_IMPORTED_MODULE_6__["default"], null)),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_DialogActions__WEBPACK_IMPORTED_MODULE_7__["default"], null,
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_8__["default"], { onClick: () => handleClose(true), sx: { textTransform: 'none' } }, "Cancel"),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Button__WEBPACK_IMPORTED_MODULE_8__["default"], { type: "submit", sx: { textTransform: 'none' } }, "Create")))));
}


/***/ }),

/***/ "./lib/components/AddButton.js":
/*!*************************************!*\
  !*** ./lib/components/AddButton.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ AddButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_AddCircleOutlineRounded__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/icons-material/AddCircleOutlineRounded */ "./node_modules/@mui/icons-material/esm/AddCircleOutlineRounded.js");



function AddButton({ handleClickButton }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { onClick: handleClickButton, size: "small" },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_AddCircleOutlineRounded__WEBPACK_IMPORTED_MODULE_2__["default"], null)));
}


/***/ }),

/***/ "./lib/components/ChartWrapper.js":
/*!****************************************!*\
  !*** ./lib/components/ChartWrapper.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DEFAULT_REFRESH_RATE: () => (/* binding */ DEFAULT_REFRESH_RATE),
/* harmony export */   "default": () => (/* binding */ ChartWrapper)
/* harmony export */ });
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _NumberInput__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./NumberInput */ "./lib/components/NumberInput.js");
/* harmony import */ var _RefreshButton__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./RefreshButton */ "./lib/components/RefreshButton.js");




const DEFAULT_REFRESH_RATE = 2;
function debounce(func, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => func(...args), delay);
    };
}
function ChartWrapper({ src, width, height }) {
    const iframeRef = react__WEBPACK_IMPORTED_MODULE_1___default().useRef(null);
    const [refreshRateS, setRefreshRateS] = react__WEBPACK_IMPORTED_MODULE_1___default().useState(DEFAULT_REFRESH_RATE);
    const initialSrcWithRefresh = `${src}&refresh=${refreshRateS}s`;
    const [iframeSrc, setIframeSrc] = react__WEBPACK_IMPORTED_MODULE_1___default().useState(initialSrcWithRefresh);
    react__WEBPACK_IMPORTED_MODULE_1___default().useEffect(() => {
        setIframeSrc(prevState => {
            const base = prevState.split('&refresh=')[0];
            return `${base}&refresh=${refreshRateS}s`;
        });
    }, [refreshRateS]);
    function handleRefreshClick() {
        // alert('Refreshing...');
        if (iframeRef.current) {
            const copy_src = structuredClone(iframeRef.current.src);
            iframeRef.current.src = copy_src;
        }
    }
    // Call the debounced function on number change
    function handleNumberChange(value) {
        const parsedValue = Number(value);
        if (!isNaN(parsedValue)) {
            debouncedSetRefreshRateS(parsedValue);
        }
    }
    // Create a debounced version of setRefreshRateS
    // Using 200ms delay instead of 2ms for a noticeable debounce effect.
    const debouncedSetRefreshRateS = react__WEBPACK_IMPORTED_MODULE_1___default().useMemo(() => debounce((value) => setRefreshRateS(value), 1000), []);
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("iframe", { src: iframeSrc, width: width, height: height, sandbox: "allow-scripts allow-same-origin", ref: iframeRef }),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.Grid2, null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_RefreshButton__WEBPACK_IMPORTED_MODULE_2__["default"], { handleRefreshClick: handleRefreshClick }),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_NumberInput__WEBPACK_IMPORTED_MODULE_3__["default"]
            // currentRefreshValue={refreshRateS}
            , { 
                // currentRefreshValue={refreshRateS}
                handleRefreshNumberChange: newValue => handleNumberChange(newValue) }))));
}


/***/ }),

/***/ "./lib/components/NumberInput.js":
/*!***************************************!*\
  !*** ./lib/components/NumberInput.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ NumberInput)
/* harmony export */ });
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../widget */ "./lib/widget.js");



function NumberInput({ 
// currentRefreshValue,
handleRefreshNumberChange }) {
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_0__.TextField, { id: "outlined-number", label: "Refresh(S)", type: "number", slotProps: {
            inputLabel: {
                shrink: true
            }
        }, onChange: event => handleRefreshNumberChange(event.target.value), 
        // value={currentRefreshValue}
        defaultValue: _widget__WEBPACK_IMPORTED_MODULE_2__.DEFAULT_REFRESH_RATE, size: "small", sx: { maxWidth: 90 } }));
}


/***/ }),

/***/ "./lib/components/RefreshButton.js":
/*!*****************************************!*\
  !*** ./lib/components/RefreshButton.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ RefreshButton)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_icons_material_RefreshRounded__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/icons-material/RefreshRounded */ "./node_modules/@mui/icons-material/esm/RefreshRounded.js");



function RefreshButton({ handleRefreshClick }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.IconButton, { onClick: handleRefreshClick, size: "small" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_icons_material_RefreshRounded__WEBPACK_IMPORTED_MODULE_2__["default"], null))));
}


/***/ }),

/***/ "./lib/components/SelectComponent.js":
/*!*******************************************!*\
  !*** ./lib/components/SelectComponent.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ SelectComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _mui_material_Box__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material/Box */ "./node_modules/@mui/material/Box/Box.js");
/* harmony import */ var _mui_material_Select__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @mui/material/Select */ "./node_modules/@mui/material/Select/Select.js");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_1__);




function SelectComponent() {
    // const [age, setAge] = React.useState('');
    const handleChange = (event) => {
        // setAge(event.target.value as string);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Box__WEBPACK_IMPORTED_MODULE_2__["default"], { sx: { minWidth: 120 } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.Tooltip, { title: "Temporarily disabled, demo." },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material_Select__WEBPACK_IMPORTED_MODULE_3__["default"], { labelId: "demo-simple-select-label", id: "demo-simple-select", 
                // value={age}
                value: '10', label: "Metric", onChange: handleChange, disabled: true, size: "small" },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.MenuItem, { value: 10 }, "CPU Cycles"),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.MenuItem, { value: 20 }, "Memory"),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement(_mui_material__WEBPACK_IMPORTED_MODULE_1__.MenuItem, { value: 30 }, "Heating")))));
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
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");



/**
 * Main reference: https://github.com/jupyterlab/extension-examples/blob/71486d7b891175fb3883a8b136b8edd2cd560385/react/react-widget/src/index.ts
 * And all other files in the repo.
 */
const namespaceId = 'gdapod';
/**
 * Initialization data for the GreenDIGIT JupyterLab extension.
 */
const plugin = {
    id: 'jupyterlab-greendigit',
    description: 'GreenDIGIT App',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: async (app, palette, restorer) => {
        console.log('JupyterLab extension GreenDIGIT is activated!');
        const { shell } = app;
        // Create a widget tracker
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: namespaceId
        });
        // Ensure the tracker is restored properly on refresh
        restorer.restore(tracker, {
            command: `${namespaceId}:open`,
            name: () => 'greendigit-jupyterlab'
            // when: app.restored, // Ensure restorer waits for the app to be fully restored
        });
        // Define a widget creator function
        const newWidget = async () => {
            const content = new _widget__WEBPACK_IMPORTED_MODULE_2__.MainWidget();
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            widget.id = 'greendigit-jupyterlab';
            widget.title.label = 'GreenDIGIT Dashboard';
            widget.title.closable = true;
            return widget;
        };
        // Add an application command
        const openCommand = `${namespaceId}:open`;
        app.commands.addCommand(openCommand, {
            label: 'Open GreenDIGIT Dashboard',
            execute: async () => {
                let widget = tracker.currentWidget;
                if (!widget || widget.isDisposed) {
                    widget = await newWidget();
                    // Add the widget to the tracker and shell
                    tracker.add(widget);
                    shell.add(widget, 'main');
                }
                if (!widget.isAttached) {
                    shell.add(widget, 'main');
                }
                shell.activateById(widget.id);
            }
        });
        // Add the command to the palette
        palette.addItem({ command: openCommand, category: 'Sustainability' });
        // Restore the widget if available
        if (!tracker.currentWidget) {
            const widget = await newWidget();
            tracker.add(widget);
            shell.add(widget, 'main');
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DEFAULT_REFRESH_RATE: () => (/* binding */ DEFAULT_REFRESH_RATE),
/* harmony export */   MainWidget: () => (/* binding */ MainWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @mui/material */ "webpack/sharing/consume/default/@mui/material/@mui/material");
/* harmony import */ var _mui_material__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_mui_material__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _components_AddButton__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./components/AddButton */ "./lib/components/AddButton.js");
/* harmony import */ var _components_ChartWrapper__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components/ChartWrapper */ "./lib/components/ChartWrapper.js");
/* harmony import */ var _CreateChartDialog__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./CreateChartDialog */ "./lib/CreateChartDialog.js");






// import BandHighLight from './components/BandHighLight';
// import ElementHighlights from './components/ElementHighlights';
// import MapComponent from './components/map/MapComponent';
// import VerticalLinearStepper from './components/VerticalLinearStepper';
const styles = {
    main: {
        display: 'flex',
        flexDirection: 'row',
        width: '100%',
        height: '100%',
        flexWrap: 'wrap',
        boxSizing: 'border-box',
        padding: '3px'
    },
    grid: {
        display: 'flex',
        flexDirection: 'column',
        whiteSpace: 'wrap',
        // justifyContent: 'center',
        // alignItems: 'center',
        flex: '0 1 100%',
        width: '100%'
    }
};
// function GridContent() {
//   return (
//     <Grid2 sx={{ width: '100%', px: 3, py: 5 }}>
//       <VerticalLinearStepper />
//     </Grid2>
//   );
// }
const CONFIG_BASE_URL = 'http://localhost:3000/';
const DEFAULT_REFRESH_RATE = 2;
const DEFAULT_SRC_IFRAME = `${CONFIG_BASE_URL}d-solo/ceetwcgabhgcgb/ping-go-server?orgId=1&from=1741098858351&to=1741100658351&timezone=browser&panelId=1&__feature.dashboardSceneSolo`;
/**
 * React component for a counter.
 *
 * @returns The React component
 */
const App = () => {
    const [iframeList, setIFrameList] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(null);
    const [createChartOpen, setCreateChartOpen] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(false);
    const [tempUrl, setTempUrl] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(null);
    function createIFrame({ src, height, width }) {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_ChartWrapper__WEBPACK_IMPORTED_MODULE_3__["default"], { src: src, width: width, height: height });
    }
    function handleCreateChart() {
        const iframe = createIFrame({
            src: tempUrl !== null && tempUrl !== void 0 ? tempUrl : DEFAULT_SRC_IFRAME,
            height: 200,
            width: 400
        });
        if (iframeList) {
            setIFrameList([...iframeList, iframe]);
        }
        else {
            setIFrameList([iframe]);
        }
        setTempUrl(null);
    }
    function handleOpenCreateChartDialog() {
        setCreateChartOpen(true);
    }
    function handleCreateChartDialogClose() {
        setCreateChartOpen(false);
        handleCreateChart();
    }
    // function handleRemoveChart()
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: styles.main },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_mui_material__WEBPACK_IMPORTED_MODULE_2__.Paper, { style: styles.grid },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_AddButton__WEBPACK_IMPORTED_MODULE_4__["default"], { handleClickButton: handleOpenCreateChartDialog }),
            iframeList ? iframeList : null),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_CreateChartDialog__WEBPACK_IMPORTED_MODULE_5__["default"], { open: createChartOpen, handleClose: (isCancel) => !isCancel && handleCreateChartDialogClose(), sendNewUrl: setTempUrl })));
};
/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
class MainWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    /**
     * Constructs a new CounterWidget.
     */
    constructor() {
        super();
        this.addClass('jp-ReactWidget');
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(App, null);
    }
}


/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/AddCircleOutlineRounded.js":
/*!*************************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/AddCircleOutlineRounded.js ***!
  \*************************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M12 7c-.55 0-1 .45-1 1v3H8c-.55 0-1 .45-1 1s.45 1 1 1h3v3c0 .55.45 1 1 1s1-.45 1-1v-3h3c.55 0 1-.45 1-1s-.45-1-1-1h-3V8c0-.55-.45-1-1-1m0-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2m0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8"
}), 'AddCircleOutlineRounded'));

/***/ }),

/***/ "./node_modules/@mui/icons-material/esm/RefreshRounded.js":
/*!****************************************************************!*\
  !*** ./node_modules/@mui/icons-material/esm/RefreshRounded.js ***!
  \****************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./utils/createSvgIcon.js */ "./node_modules/@mui/material/utils/createSvgIcon.js");
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "./node_modules/react/jsx-runtime.js");
"use client";



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ((0,_utils_createSvgIcon_js__WEBPACK_IMPORTED_MODULE_1__["default"])(/*#__PURE__*/(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("path", {
  d: "M17.65 6.35c-1.63-1.63-3.94-2.57-6.48-2.31-3.67.37-6.69 3.35-7.1 7.02C3.52 15.91 7.27 20 12 20c3.19 0 5.93-1.87 7.21-4.56.32-.67-.16-1.44-.9-1.44-.37 0-.72.2-.88.53-1.13 2.43-3.84 3.97-6.8 3.31-2.22-.49-4.01-2.3-4.48-4.52C5.31 9.44 8.26 6 12 6c1.66 0 3.14.69 4.22 1.78l-1.51 1.51c-.63.63-.19 1.71.7 1.71H19c.55 0 1-.45 1-1V6.41c0-.89-1.08-1.34-1.71-.71z"
}), 'RefreshRounded'));

/***/ })

}]);
//# sourceMappingURL=lib_index_js.0754b42bf004f8f41753.js.map