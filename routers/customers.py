from fastapi import APIRouter, Depends, HTTPException, Response

from schemas.customers import (
    CustomerAddressCreate,
    CustomerAddressResponse,
    CustomerCreate,
    CustomerDeleteRequest,
    CustomerDeleteResponse,
    CustomerResponse,
)

from security import require_api_key

from services.customers import (
    create_customer,
    create_customer_address,
    delete_customer,
    get_customer,
    get_customer_address,
    list_customers,
    list_customer_orders,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(require_api_key)],
)


@router.post("", response_model=CustomerResponse, status_code=201)
def post_customer(customer: CustomerCreate):
    return create_customer(
        first_name=customer.first_name,
        last_name=customer.last_name,
        email_encrypted=customer.email,
        phone_encrypted=customer.phone,
    )


@router.get("", response_model=list[CustomerResponse])
def read_customers():
    return list_customers()


@router.delete("", response_model=CustomerDeleteResponse, status_code=200)
def delete_customers(request: CustomerDeleteRequest):
    results = []
    deleted_count = 0
    failed_count = 0

    for customer_id in request.customer_ids:
        try:
            deleted = delete_customer(customer_id)

        except ValueError as exc:
            failed_count += 1
            results.append(
                {
                    "customer_id": customer_id,
                    "status": "failed",
                    "message": str(exc),
                }
            )
            continue

        if not deleted:
            failed_count += 1
            results.append(
                {
                    "customer_id": customer_id,
                    "status": "not_found",
                    "message": "Customer not found",
                }
            )
            continue

        deleted_count += 1
        results.append(
            {
                "customer_id": customer_id,
                "status": "deleted",
                "message": f"Customer {customer_id} was successfully deleted",
            }
        )

    return {
        "deleted_count": deleted_count,
        "failed_count": failed_count,
        "results": results,
    }


@router.get("/{customer_id}/orders")
def read_customer_orders(customer_id: str):
    customer = get_customer(customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return list_customer_orders(customer_id)


@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: str):
    customer = get_customer(customer_id)

    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.delete("/{customer_id}", status_code=200)
def delete_customer_record(customer_id: str):
    try:
        deleted = delete_customer(customer_id)

    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return {"message": f"Customer {customer_id} was successfully deleted"}


@router.post(
    "/{customer_id}/addresses",
    response_model=CustomerAddressResponse,
    status_code=201,
)
def post_customer_address(
    customer_id: str,
    address: CustomerAddressCreate,
):
    try:
        return create_customer_address(
            customer_id=customer_id,
            address_line1_encrypted=address.address_line1,
            address_line2_encrypted=address.address_line2,
            city=address.city,
            state=address.state,
            postal_code_encrypted=address.postal_code,
            country=address.country,
        )

    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/addresses/{address_id}",
    response_model=CustomerAddressResponse,
)
def read_customer_address(address_id: str):
    address = get_customer_address(address_id)

    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")

    return address
