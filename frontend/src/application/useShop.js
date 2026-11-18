import { useCallback, useEffect, useState } from "react";
import { addToCart, cartTotal, emptyCart, removeFromCart, toOrderItems } from "../domain/cart";

export function useShop(api) {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState(emptyCart);
  const [message, setMessage] = useState(null);

  const refresh = useCallback(() => api.listProducts().then(setProducts), [api]);
  useEffect(() => { refresh(); }, [refresh]);

  const checkout = async (email) => {
    try {
      const order = await api.placeOrder(email, toOrderItems(cart));
      setMessage({ type: "ok", text: `Pedido #${order.id} confirmado por $${order.total.toFixed(2)}` });
      setCart(emptyCart);
      await refresh();
    } catch (error) {
      setMessage({ type: "error", text: error.message });
    }
  };

  return {
    products, cart, message, total: cartTotal(cart),
    add: (product) => setCart((c) => addToCart(c, product)),
    remove: (id) => setCart((c) => removeFromCart(c, id)),
    checkout,
  };
}
