export default function ProductGrid({ products, onAdd }) {
  return (
    <section className="grid" aria-label="Productos">
      {products.map((product) => (
        <article key={product.id} className="product">
          <h3>{product.name}</h3>
          <p className="price">${product.price.toFixed(2)}</p>
          <p className="stock">{product.stock > 0 ? `${product.stock} disponibles` : "Agotado"}</p>
          <button disabled={product.stock === 0} onClick={() => onAdd(product)}>
            Añadir al carrito
          </button>
        </article>
      ))}
    </section>
  );
}
