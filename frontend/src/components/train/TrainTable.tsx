import { css } from "@emotion/react";
import { observer } from "mobx-react";
import { List, ListItem, ListItemText, IconButton } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { Train } from "@src/store/type";

export default function TrainTable(props: { trains: Train[] }) {
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
