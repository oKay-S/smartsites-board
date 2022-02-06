import impacket
import hashlib
from impacket.ImpactDecoder import RadioTapDecoder


class Scan:
    DECODER = RadioTapDecoder()

    def packet_handler(self, header, data):
        radio_packet = self.DECODER.decode(data)
        dot11 = radio_packet.child()
        management_base = dot11.child()
        if management_base.__class__ == impacket.dot11.Dot11DataFrame:
            s_address = management_base.get_address1()
            #   d_address = management_base.get_destination_address()

            parsed_s_address = "".join('{:02x}:'.format(x) for x in s_address)[:-1]
            parsed_s_address_stringed = parsed_s_address.encode("utf-8")
            parsed_s_address_hashed = hashlib.sha512(parsed_s_address_stringed).hexdigest()

            return parsed_s_address_hashed


