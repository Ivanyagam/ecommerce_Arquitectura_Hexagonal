import { useShop } from "./application/useShop";
import { httpShopApi } from "./infrastructure/httpShopApi";
import CartPanel from "./components/CartPanel";
import ProductGrid from "./components/ProductGrid";

export default function App() {
  const shop = useShop(httpShopApi); // raíz de composición del frontend

  return (
    <main className="layout">
      <header><h1>Tienda Hexagonal</h1></header>
      <ProductGrid products={shop.products} onAdd={shop.add} />
      <CartPanel cart={shop.cart} total={shop.total} message={shop.message}
                 onRemove={shop.remove} onCheckout={shop.checkout} />
    </main>
  );
}
