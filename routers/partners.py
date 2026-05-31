from fastapi import APIRouter, HTTPException, Depends
from psycopg.rows import dict_row

from db import get_connection, q
from schemas.partners import PartnerCreate, PartnerResponse, PartnerUpdate

from security import require_api_key

router = APIRouter(
    prefix="/partners", tags=["Partners"], dependencies=[Depends(require_api_key)]
)


def generate_partner_id(conn) -> str:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("""
            update id_counters
            set last_value = last_value + 1
            where prefix = 'PT'
            returning last_value
            """)
        result = cur.fetchone()

    if not result:
        raise HTTPException(
            status_code=500, detail="Partner ID counter is not initialized"
        )

    return f"PT{result['last_value']:05d}"


@router.post("", response_model=PartnerResponse, status_code=201)
def create_partner(partner: PartnerCreate):
    with get_connection() as conn:
        partner_id = generate_partner_id(conn)

        try:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    insert into partners (
                        partner_id,
                        partner_name,
                        contact_email,
                        feed_type,
                        default_file_format
                    )
                    values (%s, %s, %s, %s, %s)
                    returning *
                    """,
                    (
                        partner_id,
                        partner.partner_name,
                        partner.contact_email,
                        partner.feed_type,
                        partner.default_file_format,
                    ),
                )
                created_partner = cur.fetchone()

            conn.commit()
            return created_partner

        except Exception:
            conn.rollback()
            raise


@router.get("", response_model=list[PartnerResponse])
def list_partners():
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                select *
                from partners
                order by created_at desc
                """)
            return cur.fetchall()


@router.get("/{partner_id}", response_model=PartnerResponse)
def get_partner(partner_id: str):
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                select *
                from partners
                where partner_id = %s
                """,
                (partner_id,),
            )
            partner = cur.fetchone()

    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    return partner
