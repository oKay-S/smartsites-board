import impacket
import hashlib
from impacket.ImpactDecoder import RadioTapDecoder


class Scan:
    DECODER = RadioTapDecoder()

    def packet_handler(self, header, data):
        radio_packet = self.DECODER.decode(data)
        dot11 = radio_packet.child()
        management_base = dot11.child()

        addresses = []

        if management_base.__class__ == impacket.dot11.Dot11DataFrame:
            s_address = management_base.get_address1()
            p_address = management_base.get_address2()
            d_address = management_base.get_address3()

            parsed_s_address = "".join('{:02x}:'.format(x) for x in s_address)[:-1]
            parsed_s_address_stringed = parsed_s_address.encode("utf-8")
            parsed_s_address_stringed_upper = parsed_s_address_stringed.upper()
            parsed_s_address_hashed = hashlib.sha512(parsed_s_address_stringed_upper).hexdigest()

            parsed_p_address = "".join('{:02x}:'.format(x) for x in p_address)[:-1]
            parsed_p_address_stringed = parsed_p_address.encode("utf-8")
            parsed_p_address_stringed_upper = parsed_p_address_stringed.upper()
            parsed_p_address_hashed = hashlib.sha512(parsed_p_address_stringed_upper).hexdigest()

            parsed_d_address = "".join('{:02x}:'.format(x) for x in d_address)[:-1]
            parsed_d_address_stringed = parsed_d_address.encode("utf-8")
            parsed_d_address_stringed_upper = parsed_d_address_stringed.upper()
            parsed_d_address_hashed = hashlib.sha512(parsed_d_address_stringed_upper).hexdigest()

            addresses.append(parsed_s_address_hashed)
            addresses.append(parsed_p_address_hashed)
            addresses.append(parsed_d_address_hashed)

            return addresses

        elif management_base.__class__ == impacket.dot11.Dot11ManagementFrame:

            s_address = management_base.get_source_address()
            d_address = management_base.get_destination_address()

            parsed_s_address = "".join('{:02x}:'.format(x) for x in s_address)[:-1]
            parsed_s_address_stringed = parsed_s_address.encode("utf-8")
            parsed_s_address_stringed_upper = parsed_s_address_stringed.upper()
            parsed_s_address_hashed = hashlib.sha512(parsed_s_address_stringed_upper).hexdigest()

            parsed_d_address = "".join('{:02x}:'.format(x) for x in d_address)[:-1]
            parsed_d_address_stringed = parsed_d_address.encode("utf-8")
            parsed_d_address_stringed_upper = parsed_d_address_stringed.upper()
            parsed_d_address_hashed = hashlib.sha512(parsed_d_address_stringed_upper).hexdigest()

            addresses.append(parsed_s_address_hashed)
            addresses.append(parsed_d_address_hashed)

            return addresses

        elif management_base.__class__ == impacket.dot11.Dot11ControlFrameCFEndCFACK:
            address = management_base.get_ra()

            parsed_address = "".join('{:02x}:'.format(x) for x in address)[:-1]
            parsed_address_stringed = parsed_address.encode("utf-8")
            parsed_address_stringed_upper = parsed_address_stringed.upper()
            parsed_address_hashed = hashlib.sha512(parsed_address_stringed_upper).hexdigest()

            addresses.append(parsed_address_hashed)

            return addresses

        elif management_base.__class__ == impacket.dot11.Dot11ControlFrameRTS:
            address = management_base.get_ra()

            parsed_address = "".join('{:02x}:'.format(x) for x in address)[:-1]
            parsed_address_stringed = parsed_address.encode("utf-8")
            parsed_address_stringed_upper = parsed_address_stringed.upper()
            parsed_address_hashed = hashlib.sha512(parsed_address_stringed_upper).hexdigest()

            addresses.append(parsed_address_hashed)

            return addresses

        elif management_base.__class__ == impacket.dot11.Dot11ControlFrameCFEnd:
            address = management_base.get_ra()

            parsed_address = "".join('{:02x}:'.format(x) for x in address)[:-1]
            parsed_address_stringed = parsed_address.encode("utf-8")
            parsed_address_stringed_upper = parsed_address_stringed.upper()
            parsed_address_hashed = hashlib.sha512(parsed_address_stringed_upper).hexdigest()

            addresses.append(parsed_address_hashed)

            return addresses

        elif management_base.__class__ == impacket.dot11.Dot11ControlFramePSPoll:
            address = management_base.get_ta()

            parsed_address = "".join('{:02x}:'.format(x) for x in address)[:-1]
            parsed_address_stringed = parsed_address.encode("utf-8")
            parsed_address_stringed_upper = parsed_address_stringed.upper()
            parsed_address_hashed = hashlib.sha512(parsed_address_stringed_upper).hexdigest()

            addresses.append(parsed_address_hashed)

            return addresses

        elif management_base.__class__ == impacket.dot11.Dot11ControlFrameACK:
                s_address = management_base.get_ta()
                d_address = management_base.get_ra()

                parsed_s_address = "".join('{:02x}:'.format(x) for x in s_address)[:-1]
                parsed_s_address_stringed = parsed_s_address.encode("utf-8")
                parsed_s_address_stringed_upper = parsed_s_address_stringed.upper()
                parsed_s_address_hashed = hashlib.sha512(parsed_s_address_stringed_upper).hexdigest()

                parsed_d_address = "".join('{:02x}:'.format(x) for x in d_address)[:-1]
                parsed_d_address_stringed = parsed_d_address.encode("utf-8")
                parsed_d_address_stringed_upper = parsed_d_address_stringed.upper()
                parsed_d_address_hashed = hashlib.sha512(parsed_d_address_stringed_upper).hexdigest()

                addresses.append(parsed_s_address_hashed)
                addresses.append(parsed_d_address_hashed)

                return addresses

        elif management_base.__class__ == impacket.dot11.Dot11ControlFrameCTS:
                s_address = management_base.get_ta()
                d_address = management_base.get_ra()

                parsed_s_address = "".join('{:02x}:'.format(x) for x in s_address)[:-1]
                parsed_s_address_stringed = parsed_s_address.encode("utf-8")
                parsed_s_address_stringed_upper = parsed_s_address_stringed.upper()
                parsed_s_address_hashed = hashlib.sha512(parsed_s_address_stringed_upper).hexdigest()

                parsed_d_address = "".join('{:02x}:'.format(x) for x in d_address)[:-1]
                parsed_d_address_stringed = parsed_d_address.encode("utf-8")
                parsed_d_address_stringed_upper = parsed_d_address_stringed.upper()
                parsed_d_address_hashed = hashlib.sha512(parsed_d_address_stringed_upper).hexdigest()

                addresses.append(parsed_s_address_hashed)
                addresses.append(parsed_d_address_hashed)

                return addresses