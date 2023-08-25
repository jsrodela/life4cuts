from PySide6.QtCore import Qt, QSizeF
from PySide6.QtPrintSupport import QPrinter, QPrinterInfo
from PySide6.QtGui import QImage, QImageReader, QPainter, QPageLayout, QPageSize


def print_file(file_path, copy_count):
    # 기본 프린터 정보 가져오기
    default_printer = QPrinterInfo.defaultPrinter()
    if (default_printer.isNull()):
        print('연결된 프린터가 없습니다.')
        return False
    else:
        print('연결된 프린터 : ' + QPrinterInfo.defaultPrinterName())

    # 프린터 생성
    printer = QPrinter(default_printer, mode=QPrinter.HighResolution)

    print("asdf")
    # 인쇄 매수 설정
    printer.setCopyCount(copy_count)
    # 페이지 크기 설정 (A4)
    printer.setPageSize(QSizeF(4, 6))
    # 페이지 방향 설정 (가로)
    printer.setPageOrientation(QPageLayout.Orientation.Landscape)
    # DPI 설정(해상도)
    printer.setResolution(96)

    # 이미지 용량이 큰 경우 메모리 제한 해제
    QImageReader.setAllocationLimit(0)

    img = QImage(file_path)
    scaled_img = img.scaled(printer.pageRect(QPrinter.DevicePixel).width(),
                            printer.pageRect(QPrinter.DevicePixel).height(), aspectMode=Qt.KeepAspectRatio,
                            mode=Qt.SmoothTransformation)
    painter = QPainter()
    painter.begin(printer)
    painter.drawImage(0, 0, scaled_img)
    painter.end()

    print("프린트 완료")

print_file("img.png", 1)
