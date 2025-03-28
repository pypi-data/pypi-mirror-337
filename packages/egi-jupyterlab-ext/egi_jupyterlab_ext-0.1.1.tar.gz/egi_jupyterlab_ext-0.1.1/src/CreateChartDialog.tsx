import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import SelectComponent from './components/SelectComponent';

interface IFormDialog {
  open: boolean;
  handleClose: (cancel: boolean) => void;
  sendNewUrl: (url: string) => void;
}

const URL_GRAFANA_KEY = 'url_grafana';

export default function CreateChartDialog({
  open,
  handleClose,
  sendNewUrl
}: IFormDialog) {
  return (
    <React.Fragment>
      <Dialog
        open={open}
        onClose={(_e, reason) => {
          if (reason === 'backdropClick' || reason === 'escapeKeyDown') {
            return;
          } else {
            handleClose(false);
          }
        }}
        slotProps={{
          paper: {
            component: 'form',
            onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
              event.preventDefault();
              const formData = new FormData(event.currentTarget);
              const formJson = Object.fromEntries((formData as any).entries());
              if (URL_GRAFANA_KEY in formJson) {
                const url = formJson.url_grafana;
                sendNewUrl(url);
                handleClose(false);
              } else {
                throw 'Some error happened with the form.';
              }
            }
          }
        }}
      >
        <DialogTitle>Subscribe</DialogTitle>
        <DialogContent>
          <DialogContentText>
            To create a chart, you must provide the URL from the Grafana's
            dashboard.
          </DialogContentText>
          <TextField
            autoFocus
            required
            margin="dense"
            id="name"
            name={URL_GRAFANA_KEY}
            label="Grafana URL"
            type="url"
            fullWidth
            variant="outlined"
            size="small"
          />
          <SelectComponent />
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => handleClose(true)}
            sx={{ textTransform: 'none' }}
          >
            Cancel
          </Button>
          <Button type="submit" sx={{ textTransform: 'none' }}>
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}
