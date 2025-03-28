import { Grid2 } from '@mui/material';
import React from 'react';
import NumberInput from './NumberInput';
import RefreshButton from './RefreshButton';

export const DEFAULT_REFRESH_RATE = 2;

function debounce<T extends (...args: any[]) => void>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timer: ReturnType<typeof setTimeout>;
  return (...args: Parameters<T>) => {
    clearTimeout(timer);
    timer = setTimeout(() => func(...args), delay);
  };
}

interface IChartWrapper {
  src: string;
  width?: number;
  height?: number;
}
export default function ChartWrapper({ src, width, height }: IChartWrapper) {
  const iframeRef = React.useRef<HTMLIFrameElement>(null);

  const [refreshRateS, setRefreshRateS] =
    React.useState<number>(DEFAULT_REFRESH_RATE);

  const initialSrcWithRefresh = `${src}&refresh=${refreshRateS}s`;
  const [iframeSrc, setIframeSrc] = React.useState<string>(
    initialSrcWithRefresh
  );

  React.useEffect(() => {
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
  function handleNumberChange(value: string) {
    const parsedValue = Number(value);
    if (!isNaN(parsedValue)) {
      debouncedSetRefreshRateS(parsedValue);
    }
  }

  // Create a debounced version of setRefreshRateS
  // Using 200ms delay instead of 2ms for a noticeable debounce effect.
  const debouncedSetRefreshRateS = React.useMemo(
    () => debounce((value: number) => setRefreshRateS(value), 1000),
    []
  );

  return (
    <>
      <iframe
        src={iframeSrc}
        width={width}
        height={height}
        sandbox="allow-scripts allow-same-origin"
        ref={iframeRef}
      />
      <Grid2>
        <RefreshButton handleRefreshClick={handleRefreshClick} />
        <NumberInput
          // currentRefreshValue={refreshRateS}
          handleRefreshNumberChange={newValue => handleNumberChange(newValue)}
        />
      </Grid2>
    </>
  );
}
