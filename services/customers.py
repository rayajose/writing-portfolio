from __future__ import annotations

from db import (
    get_connection,
    next_address_id_with_conn,
    next_customer_id,
    q,
)

from security import (
    decrypt_pii,
    encrypt_pii,
    mask_address_line1,
    mask_email,
    mask_phone,
    mask_postal_code,
)


def create_customer(
    first_name: str,
    last_name: str,
    email_encrypted: str,
    phone_encrypted: str | None = None,
) -> dict:
    customer_id = next_customer_id()

    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                q("""
                    INSERT INTO customers (
                        customer_id,
                        first_name,
                        last_name,
                        email_encrypted,
                        phone_encrypted
                    )
                    VALUES (?, ?, ?, ?, ?)
                """),
                (
                    customer_id,
                    first_name,
                    last_name,
                    encrypt_pii(email_encrypted),
                    encrypt_pii(phone_encrypted),
                ),
            )

            conn.commit()

            return get_customer(customer_id)

        finally:
            cur.close()


def get_customer(customer_id: str) -> dict | None:
    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                q("""
                    SELECT
                        customer_id,
                        first_name,
                        last_name,
                        email_encrypted,
                        phone_encrypted,
                        created_at,
                        updated_at
                    FROM customers
                    WHERE customer_id = ?
                """),
                (customer_id,),
            )

            row = cur.fetchone()

            if row is None:
                return None

            customer = dict(row)

            try:
                decrypted_email = decrypt_pii(customer["email_encrypted"])
            except Exception:
                decrypted_email = customer["email_encrypted"]

            try:
                decrypted_phone = decrypt_pii(customer["phone_encrypted"])
            except Exception:
                decrypted_phone = customer["phone_encrypted"]

            customer["email_masked"] = mask_email(decrypted_email)
            customer["phone_masked"] = mask_phone(decrypted_phone)

            customer.pop("email_encrypted", None)
            customer.pop("phone_encrypted", None)

            return customer

        finally:
            cur.close()


def list_customers():
    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(q("""
                    SELECT
                        customer_id,
                        first_name,
                        last_name,
                        email_encrypted,
                        phone_encrypted,
                        created_at,
                        updated_at
                    FROM customers
                    ORDER BY customer_id
                """))

            rows = cur.fetchall()

            customers = []

            for row in rows:
                customer = dict(row)

                try:
                    decrypted_email = decrypt_pii(customer["email_encrypted"])
                except Exception:
                    decrypted_email = customer["email_encrypted"]

                try:
                    decrypted_phone = decrypt_pii(customer["phone_encrypted"])
                except Exception:
                    decrypted_phone = customer["phone_encrypted"]

                customer["email_masked"] = mask_email(decrypted_email)

                customer["phone_masked"] = mask_phone(decrypted_phone)

                customer.pop("email_encrypted", None)
                customer.pop("phone_encrypted", None)

                customers.append(customer)

            return customers

        finally:
            cur.close()


def create_customer_address(
    customer_id: str,
    address_line1_encrypted: str,
    city: str,
    state: str,
    postal_code_encrypted: str,
    address_line2_encrypted: str | None = None,
    country: str = "US",
) -> dict:
    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                q("""
                    SELECT customer_id
                    FROM customers
                    WHERE customer_id = ?
                """),
                (customer_id,),
            )

            if cur.fetchone() is None:
                raise ValueError(f"Customer not found: {customer_id}")

            address_id = next_address_id_with_conn(conn)

            cur.execute(
                q("""
                    INSERT INTO customer_addresses (
                        address_id,
                        customer_id,
                        address_line1_encrypted,
                        address_line2_encrypted,
                        city,
                        state,
                        postal_code_encrypted,
                        country
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """),
                (
                    address_id,
                    customer_id,
                    encrypt_pii(address_line1_encrypted),
                    encrypt_pii(address_line2_encrypted),
                    city,
                    state,
                    encrypt_pii(postal_code_encrypted),
                    country,
                ),
            )

            conn.commit()

            return get_customer_address(address_id)

        finally:
            cur.close()


def get_customer_address(
    address_id: str,
) -> dict | None:
    with get_connection() as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                q("""
                    SELECT
                        address_id,
                        customer_id,
                        address_line1_encrypted,
                        address_line2_encrypted,
                        city,
                        state,
                        postal_code_encrypted,
                        country,
                        created_at
                    FROM customer_addresses
                    WHERE address_id = ?
                """),
                (address_id,),
            )

            row = cur.fetchone()

            if row is None:
                return None

            address = dict(row)

            decrypted_address_line1 = decrypt_pii(address["address_line1_encrypted"])

            decrypted_postal_code = decrypt_pii(address["postal_code_encrypted"])

            address["address_line1_masked"] = mask_address_line1(
                decrypted_address_line1
            )

            address["postal_code_masked"] = mask_postal_code(decrypted_postal_code)

            address.pop("address_line1_encrypted", None)
            address.pop("address_line2_encrypted", None)
            address.pop("postal_code_encrypted", None)

            return address

        finally:
            cur.close()
