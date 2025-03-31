use pyo3::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq)]
#[pyclass(eq, eq_int)]
pub enum UnaryOperator {
    Not,
    IsNull,
    IsNotNull,
}

impl Into<topk_protos::v1::data::logical_expr::unary_op::Op> for UnaryOperator {
    fn into(self) -> topk_protos::v1::data::logical_expr::unary_op::Op {
        match self {
            UnaryOperator::Not => topk_protos::v1::data::logical_expr::unary_op::Op::Not,
            UnaryOperator::IsNull => topk_protos::v1::data::logical_expr::unary_op::Op::IsNull,
            UnaryOperator::IsNotNull => {
                topk_protos::v1::data::logical_expr::unary_op::Op::IsNotNull
            }
        }
    }
}
