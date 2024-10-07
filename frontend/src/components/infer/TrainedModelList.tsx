import { css } from "@emotion/react";
import { List, ListItem, ListItemText, IconButton } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { TrainedModel } from "@src/store/type";

export default function TrainedModelList(props: { trainedModels: TrainedModel[] }) {
  return (
    <>
      <List>
        <ListItem
          secondaryAction={
            <IconButton edge="end" aria-label="delete">
              <DeleteIcon />
            </IconButton>
          }
        >
          <ListItemText primary="Single-line item" />
          <ListItemText primary="Single-line item" />
        </ListItem>
      </List>
    </>
  );
}
