import { useState } from "react";

export default function CartPanel({ cart, total, message, onRemove, onCheckout }) {
  const [email, setEmail] = useState("");

  return (
    <aside className="cart">
      <h2>Tu carrito</h2>
      {cart.length === 0 && <p>Añade productos para empezar tu pedido.</p>}
      <ul>
        {cart.map(({ product, quantity }) => (
          <li key={product.id}>
            <span>{quantity} × {product.name}</span>
            <button className="link" onClick={() => onRemove(product.id)}>Quitar</button>
          </li>
        ))}
      </ul>
      <p className="total">Total: ${total.toFixed(2)}</p>
      <input type="email" placeholder="Tu correo" value={email}
             onChange={(e) => setEmail(e.target.value)} />
      <button disabled={!cart.length || !email} onClick={() => onCheckout(email)}>
        Confirmar pedido
      </button>
      {message && <p className={`msg ${message.type}`} role="status">{message.text}</p>}
    </aside>
  );
}
