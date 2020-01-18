import React from "react";
import { Link } from "react-router-dom";
import { Link as MaterialLink } from "@material-ui/core";

export default function CustomLink({ to, children }) {
  return (
    <Link to={to} component={MaterialLink}>
      {children}
    </Link>
  );
}
