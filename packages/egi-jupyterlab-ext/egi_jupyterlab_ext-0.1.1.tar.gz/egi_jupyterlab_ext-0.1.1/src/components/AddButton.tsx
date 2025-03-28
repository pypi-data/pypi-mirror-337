import React from 'react';
import { IconButton } from '@mui/material';
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';

interface IAddButton {
  handleClickButton: () => void;
}

export default function AddButton({ handleClickButton }: IAddButton) {
  return (
    <IconButton onClick={handleClickButton} size="small">
      <AddCircleOutlineRoundedIcon />
    </IconButton>
  );
}
