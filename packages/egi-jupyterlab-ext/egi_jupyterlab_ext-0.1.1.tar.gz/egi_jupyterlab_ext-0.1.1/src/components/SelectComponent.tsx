import * as React from 'react';
import Box from '@mui/material/Box';

import Select, { SelectChangeEvent } from '@mui/material/Select';
import { MenuItem, Tooltip } from '@mui/material';

export default function SelectComponent() {
  // const [age, setAge] = React.useState('');

  const handleChange = (event: SelectChangeEvent) => {
    // setAge(event.target.value as string);
  };

  return (
    <Box sx={{ minWidth: 120 }}>
      <Tooltip title="Temporarily disabled, demo.">
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          // value={age}
          value={'10'}
          label="Metric"
          onChange={handleChange}
          disabled
          size="small"
        >
          <MenuItem value={10}>CPU Cycles</MenuItem>
          <MenuItem value={20}>Memory</MenuItem>
          <MenuItem value={30}>Heating</MenuItem>
        </Select>
      </Tooltip>
    </Box>
  );
}
