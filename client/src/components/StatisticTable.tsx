import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { IOrder } from "interfaces/orders/interface";

interface IProps {
  orders: IOrder[];
  averagePrice?: string;
  totalQuantity?: string;
  tpPrice?: string;
  expectedProfit?: string;
  totalSpent?: string;
}

const StatisticTable = ({
  orders,
  averagePrice,
  totalQuantity,
  tpPrice,
  expectedProfit,
  totalSpent,
}: IProps) => {
  if (!orders?.length) return null;

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead></TableHead>
          <TableHead className="text-center">Avg Price</TableHead>
          <TableHead className="text-center">Take Profit Price</TableHead>
          <TableHead className="text-center">Expected Profit</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow>
          <TableCell
            className={`text-center text-white  bg-purple-800 border-l-[1px]  border-r-[1px]`}
          >
            Total spent
          </TableCell>
          <TableCell
            className={`text-center text-white border-r-[1px] border-b-[1px] `}
            rowSpan={4}
          >
            ${averagePrice}
          </TableCell>
          <TableCell
            className={`text-center text-white border-r-[1px] border-b-[1px]`}
            rowSpan={4}
          >
            ${tpPrice}
          </TableCell>
          <TableCell
            className={`text-center text-white border-r-[1px] border-b-[1px]`}
            rowSpan={4}
          >
            ${expectedProfit}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell
            className={`text-center text-white bg-purple-400 border-l-[1px]  border-r-[1px]`}
          >
            ${totalSpent}
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell
            className={`text-center text-white  bg-purple-800 border-l-[1px]  border-r-[1px]`}
          >
            Total quantity
          </TableCell>
        </TableRow>
        <TableRow>
          <TableCell
            className={`text-center text-white bg-purple-400 border-l-[1px] border-b-[1px]  border-r-[1px]`}
          >
            {totalQuantity}
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  );
};

export default StatisticTable;
