import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
import { Paper } from '@mui/material';
import AddButton from './components/AddButton';
import ChartWrapper from './components/ChartWrapper';
import CreateChartDialog from './CreateChartDialog';

// import BandHighLight from './components/BandHighLight';
// import ElementHighlights from './components/ElementHighlights';
// import MapComponent from './components/map/MapComponent';
// import VerticalLinearStepper from './components/VerticalLinearStepper';

const styles: Record<string, React.CSSProperties> = {
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
export const DEFAULT_REFRESH_RATE = 2;

interface ICreateIFrame {
  src: string;
  height: number;
  width: number;
}

const DEFAULT_SRC_IFRAME = `${CONFIG_BASE_URL}d-solo/ceetwcgabhgcgb/ping-go-server?orgId=1&from=1741098858351&to=1741100658351&timezone=browser&panelId=1&__feature.dashboardSceneSolo`;

/**
 * React component for a counter.
 *
 * @returns The React component
 */
const App = (): JSX.Element => {
  const [iframeList, setIFrameList] = React.useState<
    React.JSX.Element[] | null
  >(null);
  const [createChartOpen, setCreateChartOpen] = React.useState<boolean>(false);
  const [tempUrl, setTempUrl] = React.useState<string | null>(null);

  function createIFrame({ src, height, width }: ICreateIFrame) {
    return <ChartWrapper src={src} width={width} height={height} />;
  }

  function handleCreateChart() {
    const iframe = createIFrame({
      src: tempUrl ?? DEFAULT_SRC_IFRAME,
      height: 200,
      width: 400
    });

    if (iframeList) {
      setIFrameList([...iframeList, iframe]);
    } else {
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

  return (
    <div style={styles.main}>
      <Paper style={styles.grid}>
        <AddButton handleClickButton={handleOpenCreateChartDialog} />

        {iframeList ? iframeList : null}
      </Paper>
      <CreateChartDialog
        open={createChartOpen}
        handleClose={(isCancel: boolean) =>
          !isCancel && handleCreateChartDialogClose()
        }
        sendNewUrl={setTempUrl}
      />
    </div>
  );
};

/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
export class MainWidget extends ReactWidget {
  /**
   * Constructs a new CounterWidget.
   */
  constructor() {
    super();
    this.addClass('jp-ReactWidget');
  }

  render(): JSX.Element {
    return <App />;
  }
}
