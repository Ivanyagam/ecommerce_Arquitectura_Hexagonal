export const emptyCart = [];

export const addToCart = (cart, product) => {
  const existing = cart.find((line) => line.product.id === product.id);
  if (!existing) return [...cart, { product, quantity: 1 }];
  return cart.map((line) =>
    line === existing ? { ...line, quantity: line.quantity + 1 } : line
  );
};

export const removeFromCart = (cart, productId) =>
  cart.filter((line) => line.product.id !== productId);

export const cartTotal = (cart) =>
  cart.reduce((sum, { product, quantity }) => sum + product.price * quantity, 0);

export const toOrderItems = (cart) =>
  cart.map(({ product, quantity }) => ({ productId: product.id, quantity }));
