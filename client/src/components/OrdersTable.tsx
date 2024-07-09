import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ORDER_SIDE } from "interfaces/orders/enum";
import { IOrder } from "interfaces/orders/interface";

interface IProps {
  orders: IOrder[];
}

const OrdersTable = ({ orders }: IProps) => {
  if (!orders) throw new Error("No orders data");

  const getCellColor = (side: ORDER_SIDE) => {
    switch (side) {
      case "BUY":
        return "bg-teal-600";
      case "SELL":
        return "bg-rose-500";
      default:
        return "bg-gray-600";
    }
  };
  return (
    <Table>
      <TableCaption>A list of orders in progress</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead>Order Id</TableHead>
          <TableHead>Price</TableHead>
          <TableHead>Qty</TableHead>
          <TableHead>Commission</TableHead>
          <TableHead>Total</TableHead>
          <TableHead>Status</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {orders.map((order) => (
          <TableRow key={order.orderId}>
            <TableCell
              className={`text-left text-white ${getCellColor(order.side)}`}
            >
              {order.orderId}
            </TableCell>
            <TableCell
              className={`text-left text-white ${getCellColor(order.side)}`}
            >
              ${parseFloat(order.price).toFixed(2)}
            </TableCell>
            <TableCell
              className={`text-left text-white ${getCellColor(order.side)}`}
            >
              ${parseFloat(order.origQty).toFixed(4)}
            </TableCell>
            <TableCell
              className={`text-left text-white ${getCellColor(order.side)}`}
            >
              {parseFloat(
                String(
                  (parseFloat(order.origQty) / 1000) * parseFloat(order.price)
                )
              ).toFixed(4)}
            </TableCell>
            <TableCell
              className={`text-left text-white ${getCellColor(order.side)}`}
            >
              $
              {parseFloat(
                String(parseFloat(order.origQty) * parseFloat(order.price))
              ).toFixed(2)}
            </TableCell>
            <TableCell
              className={`text-left text-white ${getCellColor(order.side)}`}
            >
              {order.status}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default OrdersTable;
