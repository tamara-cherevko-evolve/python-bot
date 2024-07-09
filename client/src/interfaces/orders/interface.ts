import { ORDER_SIDE, ORDER_STATUS } from "./enum";

export interface IOrdersData {
  completed_orders?: IOrder[];
  orders_are_listening?: IOrder[];
  current_price: string;
  last_update: Date;
  average_price: string;
  total_quantity: string;
  tp_price: string;
  expected_profit: string;
  total_spent: string;
}

export interface IOrder {
  symbol: string;
  orderId: number;
  orderListId: number;
  clientOrderId: string;
  price: string;
  origQty: string;
  executedQty: string;
  cummulativeQuoteQty: string;
  status: ORDER_STATUS;
  timeInForce: string;
  type: "LIMIT";
  side: ORDER_SIDE;
  stopPrice: string;
  icebergQty: string;
  time: number;
  updateTime: number;
  isWorking: true;
  workingTime: number;
  origQuoteOrderQty: string;
  selfTradePreventionMode: string;
}
