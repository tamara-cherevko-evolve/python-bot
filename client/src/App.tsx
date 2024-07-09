import { Button } from "@/components/ui/button";
import { ReactComponent as BinanceLogo } from "assets/images/binanceLogo.svg";
import "./App.css";
import OrdersTable from "components/OrdersTable";
import { IOrder, IOrdersData } from "interfaces/orders/interface";
import axios from "axios";
import { useEffect, useState } from "react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import StatisticTable from "components/StatisticTable";
import DisconnectedMessage from "components/DisconnectedMessage";
import { Badge } from "@/components/ui/badge";

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [connectionError, setConnectionError] = useState<Event | null>(null);
  const [isRecalculatingSellOrder, setIsRecalculatingSellOrder] =
    useState(false);
  const [connectionStatus, setConnectionStatus] = useState<boolean>(false);
  const [ordersData, setOrdersData] = useState<IOrdersData | null>(null);

  useEffect(() => {
    if (!connectionStatus) {
      openSocket();
    }
  }, []);

  const startHandler = async () => {
    setIsLoading(true);
    try {
      await axios.post("http://localhost:8000/start-dca-grid", {
        method: "POST",
      });
      setIsLoading(false);
    } catch (error) {
      console.log(error);
      setIsLoading(false);
    }
  };

  const recalculateSellOrderHandler = async () => {
    setIsRecalculatingSellOrder(true);
    try {
      await axios.post("http://localhost:8000/recalculate-sell-order", {
        method: "POST",
      });
      setIsRecalculatingSellOrder(false);
    } catch (error) {
      console.log(error);
      setIsRecalculatingSellOrder(false);
    }
  };

  const openSocket = async () => {
    const socket = new WebSocket("ws://localhost:8765");

    // Connection opened
    socket.onopen = function (event) {
      setConnectionError(null);
      setConnectionStatus(true);
      console.log("Connection opened", event);
    };

    // Listen for messages
    socket.onmessage = function (event) {
      setOrdersData(JSON.parse(event.data));
      console.log(JSON.parse(event.data));
    };

    // Listen for possible errors
    socket.onerror = function (error) {
      setConnectionError(error);
      setConnectionStatus(false);
      console.error("WebSocket Error", error);
    };

    // Connection closed
    socket.onclose = function (event) {
      setConnectionError(event);
      setConnectionStatus(false);
      console.log("Connection closed", event);
    };
  };

  return (
    <div className="h-full bg-gray-800 App">
      <div className="flex justify-between gap-5 mt-4 mb-8">
        <Button
          onClick={recalculateSellOrderHandler}
          className="w-[210px]"
          disabled={isRecalculatingSellOrder}
        >
          <BinanceLogo className="w-5 h-5 mr-2" />
          {isLoading ? "Loading..." : "Recalculate Sell Order"}
        </Button>
        <div className="flex justify-end gap-5">
          <div>
            <Badge
              variant="default"
              className={`${
                connectionStatus ? "bg-green-500" : "bg-gray-500"
              } text-white p-2`}
            >
              {connectionStatus ? "Connected" : "Disconnected"}
            </Badge>
          </div>
          <Button
            onClick={startHandler}
            disabled={isLoading || !!ordersData?.orders_are_listening?.length}
            className="w-[210px]"
          >
            <BinanceLogo className="w-5 h-5 mr-2" />
            {isLoading ? "Loading..." : "Start DCA Grid"}
          </Button>
        </div>
      </div>

      <div className="flex gap-10 mt-5">
        <div className="basis-1/2">
          <Card className="bg-transparent">
            <CardHeader>
              <CardTitle className="text-white">
                Filled Orders
                {connectionStatus
                  ? ` (${ordersData?.completed_orders?.length || 0})`
                  : ""}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {!connectionStatus && <DisconnectedMessage />}
              {connectionStatus && !ordersData && (
                <div className="flex space-x-8">
                  <Skeleton className="h-[200px] flex-1 rounded-xl" />
                  <Skeleton className="h-[200px] flex-1 rounded-xl" />
                  <Skeleton className="h-[200px] flex-1 rounded-xl" />
                  <Skeleton className="h-[200px] flex-1 rounded-xl" />
                </div>
              )}
              {connectionStatus && ordersData && (
                <StatisticTable
                  orders={ordersData?.completed_orders || []}
                  averagePrice={ordersData?.average_price}
                  totalQuantity={ordersData?.total_quantity}
                  tpPrice={ordersData?.tp_price}
                  expectedProfit={ordersData?.expected_profit}
                  totalSpent={ordersData?.total_spent}
                />
              )}
            </CardContent>
          </Card>
        </div>
        <div className="basis-1/2">
          <Card className="bg-transparent">
            <CardHeader>
              <CardTitle className="text-white">
                Open Orders
                {connectionStatus
                  ? ` (${
                      ordersData?.orders_are_listening?.length
                        ? ordersData.orders_are_listening.length - 1
                        : 0
                    })`
                  : ""}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {connectionStatus && ordersData && (
                <>
                  <Alert
                    className="mb-2"
                    variant={connectionStatus ? "default" : "destructive"}
                  >
                    <AlertTitle
                      className={`text-lg font-bold ${
                        connectionStatus ? "text-emerald-800" : "initial"
                      }`}
                    >
                      {parseFloat(ordersData?.current_price).toFixed(2)}
                    </AlertTitle>
                    <AlertDescription>
                      Last update: {ordersData?.last_update?.toLocaleString()}
                    </AlertDescription>
                  </Alert>
                  <OrdersTable
                    orders={
                      (ordersData?.orders_are_listening as IOrder[]) || []
                    }
                  />
                </>
              )}
              {connectionStatus && !ordersData && (
                <div className="flex flex-col space-y-8">
                  <Skeleton className="h-[100px] w-full rounded-xl" />
                  <div className="space-y-4">
                    <Skeleton className="w-full h-[50px]" />
                    <Skeleton className="w-full h-[50px]" />
                    <Skeleton className="w-full h-[50px]" />
                    <Skeleton className="w-full h-[50px]" />
                  </div>
                </div>
              )}
              {!connectionStatus && <DisconnectedMessage />}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default App;
