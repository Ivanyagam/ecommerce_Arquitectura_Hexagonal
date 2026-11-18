const request = async (url, options) => {
  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error ?? "Error inesperado");
  return data;
};

export const httpShopApi = {
  listProducts: () => request("/api/products"),
  placeOrder: (email, items) =>
    request("/api/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, items }),
    }),
};
