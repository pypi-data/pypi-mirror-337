// import { AppBar, Container, CssBaseline, IconButton, Toolbar, Typography } from '@mui/material'
// import Refresh from '@mui/icons-material/Refresh';
// import Close from '@mui/icons-material/Close';

import React from 'react'
import BasicTabs from './BasicTabs';
// import { FileManagerComponent } from '@syncfusion/ej2-react-filemanager';

interface FileManagerPanelComponentProps {
     downloadsFolder: string;
}

const FileManagerPanelComponent: React.FC<FileManagerPanelComponentProps> = (props): JSX.Element => {
     return (
          <div style={{ width: "100%", minWidth: "400px", height: "100vh" }}>
               <BasicTabs downloadsFolder={props.downloadsFolder} />
          </div>
     );
}

export default FileManagerPanelComponent;