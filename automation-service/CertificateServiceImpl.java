package com.example.automated.service.pdf;

import com.itextpdf.kernel.pdf.PdfWriter;
import com.itextpdf.kernel.pdf.PdfDocument;
import com.itextpdf.layout.Document;
import com.itextpdf.layout.element.Paragraph;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;

@Service
public class CertificateServiceImpl implements CertificateService {

    @Override
    public byte[] generateCertificate(String name) {
        try {
            ByteArrayOutputStream out = new ByteArrayOutputStream();

            PdfWriter writer = new PdfWriter(out);
            PdfDocument pdf = new PdfDocument(writer);
            Document document = new Document(pdf);

            document.add(new Paragraph("Certificate of Completion"));
            document.add(new Paragraph(" "));
            document.add(new Paragraph("This certificate is awarded to:"));
            document.add(new Paragraph(name));
            document.add(new Paragraph(" "));
            document.add(new Paragraph("For successful completion of internship."));

            document.close();

            return out.toByteArray();

        } catch (Exception e) {
            throw new RuntimeException("Error generating PDF");
        }
    }
}