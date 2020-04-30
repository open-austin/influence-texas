import React from "react";
import { render } from "@testing-library/react";
import App from "./App";

test("renders without breaking", () => {
  const { getByText } = render(<App />);
  const linkElement = getByText(/influence texas/i);
  expect(linkElement).toBeInTheDocument();
});
